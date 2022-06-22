import bpy
from mathutils import Vector
from collections import defaultdict as dd
from mathutils.kdtree import KDTree
from bpy_extras.object_utils import world_to_camera_view

C = bpy.context
D = bpy.data
receipt = D.objects["receipt"]
scene = D.scenes[0]
camera = D.objects["Camera"]


def render(size, bbs_coords):
    # set the size of our render quality
    width, height = size
    rs = scene.render
    rs.resolution_x = width
    rs.resolution_y = height
    dg = C.evaluated_depsgraph_get()
    obj = receipt.evaluated_get(dg)
    mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
    mesh.update(calc_edges=True, calc_edges_loose=True)
    mesh.calc_loop_triangles()
    vert_to_coords = {}
    vert_to_faces = dd(list)
    verts_and_coords = []
    for uv_layer in mesh.uv_layers:
        for tri in mesh.loop_triangles:
            for i in range(3):
                vert_index = tri.vertices[i]
                loop_index = tri.loops[i]
                uv = uv_layer.data[loop_index].uv
                uv_coord = Vector((uv.x, uv.y))
                vert_to_coords[vert_index] = uv_coord
                verts_and_coords.append((loop_index, uv_coord))
                vert_to_faces[vert_index].append(tri.index)
    tree_size = len(verts_and_coords)
    kdtree = KDTree(tree_size)
    for loop_index, uv_coord in verts_and_coords:
        kdtree.insert(Vector((uv_coord.x, uv_coord.y, 0)), loop_index)
    kdtree.balance()
    image_bbs = []
    for word_dict in bbs_coords:
        word_new_info = {}
        name = word_dict['word']
        bb = word_dict['polygon']
        raw_bbs = []
        for coord in bb:
            img_pos = map_coord(scene, camera, receipt.matrix_world, coord,
                                mesh, vert_to_coords, vert_to_faces, verts_and_coords, kdtree)
            img_pos = (img_pos.x, img_pos.y)
            # print(img_pos)
            raw_bbs.append(img_pos)
        # ul, br = bounding_box_for_points(raw_bbs)
        bl = norm_img_to_render_space(size, raw_bbs[0])
        ul = norm_img_to_render_space(size, raw_bbs[1])
        ur = norm_img_to_render_space(size, raw_bbs[2])
        br = norm_img_to_render_space(size, raw_bbs[3])
        word_new_info['word'] = name
        word_new_info['polygon'] = [ul, ur, br, bl]
        image_bbs.append(word_new_info)
    return image_bbs


def triangle_area(verts):
    """ computes triangle area.  it is possible to have a negative area, and is
    in fact required for barycentric coordinates to work correctly """
    a, b, c = verts[0], verts[1], verts[2]
    return (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) / 2.0


def barycentric_coords(verts, point):
    area = triangle_area(verts)
    # the face area divide the face(triangle) to 3 areas and calculate each area
    sub_area1 = triangle_area((point, verts[0], verts[1]))
    sub_area2 = triangle_area((point, verts[1], verts[2]))
    sub_area3 = triangle_area((point, verts[2], verts[0]))
    # precentage of each triangle
    x = sub_area1 / area
    y = sub_area2 / area
    z = sub_area3 / area
    coord = Vector((x, y, z))
    return coord


def bary_interpolate(coords, verts):
    interp = verts[2] * coords.x + verts[0] * coords.y + verts[1] * coords.z
    return interp


def contains_vert(face, vert):
    bcoord = barycentric_coords(face, vert)
    return (bcoord[0] <= 1.0 and bcoord[0] > 0) \
           and (bcoord[1] <= 1.0 and bcoord[1] >= 0) \
           and (bcoord[2] <= 1.0 and bcoord[2] >= 0)


def get_containing_face(mesh, vert_to_coords, vert_to_faces, verts_and_coords,
                        kdtree, point):
    # get our match index of the closest uv coordinate
    coordinate, midx, dist = kdtree.find((point.x, point.y, 0))
    # print("the coordinate,midx and dist is:",coordinate, midx, dist)

    # from our match index, get the vertex associated with our closest match
    # vidx, coord = verts_and_coords[midx]
    # print("the vidx and coord is:",vidx,coord)
    vidx = mesh.loops[midx].vertex_index
    # print("the vidx and its coordinates is:",vidx,vert_to_coords[vidx])

    # find all the faces using that vertex
    tries = vert_to_faces[vidx]
    # print("the tries are:",tries)

    # test each face individually for containing coord
    for tridx in tries:
        tri = mesh.loop_triangles[tridx]
        coords = [vert_to_coords[vidx] for vidx in tri.vertices]
        # print("the",tri,"vertices coords are",coords)
        if contains_vert(coords, point):
            # print(tridx)
            return tridx


def map_coord(scene, camera, local_world_mat, uv_coord, mesh,
              vert_to_coords, vert_to_faces, verts_and_coords, kdtree):
    """ converts a uv coord to a *NORMALIZED* image-space position """
    # get the face index that contains the uv_coord
    fidx = get_containing_face(mesh, vert_to_coords, vert_to_faces,
                               verts_and_coords, kdtree, uv_coord)
    # print("the map coord fidx is" ,fidx)
    face = mesh.loop_triangles[fidx]
    # the uv coords of all the vertices in the face, 3 vertices only
    face_uv_coords = [vert_to_coords[vidx] for vidx in face.vertices]
    # co type is float array of 3 items in [-inf, inf], maybe the mesh coordinates for vertices in face (also 3)
    face_coords = [mesh.vertices[vidx].co for vidx in face.vertices]

    bary = barycentric_coords(face_uv_coords, uv_coord)
    uv_local_coord = bary_interpolate(bary, face_coords)
    # world position
    wpos = local_world_mat @ uv_local_coord
    # Returns the camera space coords for a 3d point Where (0, 0) is the bottom left and (1, 1) is the top right
    # of the camera frame. values outside 0-1 are also supported. A negative ‘z’ value means the point is behind
    # the camera.
    # Takes shift-x/y, lens angle and sensor size into account as well as perspective/ortho projections.
    # Returns a vector where X and Y map to the view plane and Z is the depth on the view axis.
    img_pos = world_to_camera_view(scene, camera, wpos)
    return img_pos


def norm_img_to_render_space(render_size, coord):
    coord = (
        round(coord[0] * render_size[0]),
        round((1.0 - coord[1]) * render_size[1])
    )
    return coord


if __name__ == "__main__":
    print("the bb ul and br are :", render((1920, 1080)))
