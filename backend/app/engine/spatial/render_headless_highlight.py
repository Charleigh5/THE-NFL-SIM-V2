"""
Standalone Blender 5.2.1 LTS CLI Headless Highlight Renderer
Invoked via:
  blender.exe -b -P render_headless_highlight.py -- --play-id <ID> --drama-index <FLOAT> --impact-force <FLOAT> --output-path <PATH>
"""

import sys
import os
import math
import argparse

try:
    import bpy
except ImportError:
    print("ERROR: This script must be run inside Blender's python environment (blender.exe -b -P ...)")
    sys.exit(1)


def parse_args():
    # Only parse arguments after the '--' delimiter
    if "--" in sys.argv:
        args_list = sys.argv[sys.argv.index("--") + 1:]
    else:
        args_list = []

    parser = argparse.ArgumentParser(description="Blender Headless Gridiron Cutscene Renderer")
    parser.add_argument("--play-id", type=int, default=101, help="Simulated play ID")
    parser.add_argument("--drama-index", type=float, default=85.0, help="Drama index (0-100)")
    parser.add_argument("--impact-force", type=float, default=90.0, help="Orthopedic impact force (0-100)")
    parser.add_argument("--output-path", type=str, required=True, help="Output destination file path (PNG)")
    parser.add_argument("--samples", type=int, default=4, help="Cycles render samples")

    return parser.parse_args(args_list)


def build_scene(play_id: int, drama_index: float, impact_force: float, output_path: str, samples: int = 4):
    print(f"[BlenderService] Initializing headless render for Play #{play_id} (Drama={drama_index}, Force={impact_force})")

    # 1. Reset to empty scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2. Gridiron Turf Plane
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    turf = bpy.context.active_object
    turf.name = "GridironTurf"
    mat_turf = bpy.data.materials.new(name="TurfMaterial")
    mat_turf.use_nodes = True
    bsdf_turf = mat_turf.node_tree.nodes.get("Principled BSDF")
    if bsdf_turf:
        bsdf_turf.inputs["Base Color"].default_value = (0.04, 0.20, 0.05, 1.0)
        bsdf_turf.inputs["Roughness"].default_value = 0.85
    turf.data.materials.append(mat_turf)

    # 3. Yard Line Accent
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.005))
    yard_line = bpy.context.active_object
    yard_line.name = "YardLine_50"
    yard_line.scale = (0.2, 16.0, 1.0)
    mat_line = bpy.data.materials.new(name="YardLineMaterial")
    mat_line.use_nodes = True
    bsdf_line = mat_line.node_tree.nodes.get("Principled BSDF")
    if bsdf_line:
        bsdf_line.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1.0)
        bsdf_line.inputs["Roughness"].default_value = 0.4
    yard_line.data.materials.append(mat_line)

    # 4. Ball Carrier Proxy (#22, Royal Blue)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=1.85, location=(-0.35, 0.25, 0.925))
    carrier = bpy.context.active_object
    carrier.name = "Player_Carrier_22"
    carrier.rotation_euler = (math.radians(18), math.radians(-12), math.radians(45))
    mat_carrier = bpy.data.materials.new(name="CarrierMaterial")
    mat_carrier.use_nodes = True
    bsdf_c = mat_carrier.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs["Base Color"].default_value = (0.02, 0.18, 0.70, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.25
    carrier.data.materials.append(mat_carrier)

    # 5. Defensive Tackler Proxy (#54, Crimson Red)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.50, depth=1.88, location=(0.45, -0.20, 0.88))
    tackler = bpy.context.active_object
    tackler.name = "Player_Tackler_54"
    tackler.rotation_euler = (math.radians(-28), math.radians(16), math.radians(-115))
    mat_tackler = bpy.data.materials.new(name="TacklerMaterial")
    mat_tackler.use_nodes = True
    bsdf_t = mat_tackler.node_tree.nodes.get("Principled BSDF")
    if bsdf_t:
        bsdf_t.inputs["Base Color"].default_value = (0.75, 0.06, 0.10, 1.0)
        bsdf_t.inputs["Roughness"].default_value = 0.25
    tackler.data.materials.append(mat_tackler)

    # 6. Wilson NFL Football
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(-0.12, 0.65, 1.25))
    ball = bpy.context.active_object
    ball.name = "WilsonFootball"
    ball.scale = (0.8, 1.45, 0.8)
    mat_ball = bpy.data.materials.new(name="FootballMaterial")
    mat_ball.use_nodes = True
    bsdf_b = mat_ball.node_tree.nodes.get("Principled BSDF")
    if bsdf_b:
        bsdf_b.inputs["Base Color"].default_value = (0.35, 0.12, 0.04, 1.0)
        bsdf_b.inputs["Roughness"].default_value = 0.45
    ball.data.materials.append(mat_ball)

    # 7. Studio 3-Point Broadcast Lighting Rig
    # Key Light (Warm Stadium Floodlight)
    bpy.ops.object.light_add(type='SPOT', location=(6.0, -8.0, 7.5))
    key_light = bpy.context.active_object
    key_light.name = "KeyStadiumLight"
    key_light.data.energy = 2500.0
    key_light.data.color = (1.0, 0.95, 0.88)
    key_light.data.spot_size = math.radians(65)
    key_light.rotation_euler = (math.radians(50), 0, math.radians(35))

    # Fill Light (Cool Sky Light)
    bpy.ops.object.light_add(type='AREA', location=(-7.0, -5.0, 5.5))
    fill_light = bpy.context.active_object
    fill_light.name = "FillSkyLight"
    fill_light.data.energy = 900.0
    fill_light.data.color = (0.82, 0.90, 1.0)
    fill_light.rotation_euler = (math.radians(55), 0, math.radians(-50))

    # Rim / Edge Highlight Light
    bpy.ops.object.light_add(type='SPOT', location=(0.0, 7.5, 6.5))
    rim_light = bpy.context.active_object
    rim_light.name = "RimEdgeLight"
    rim_light.data.energy = 2000.0
    rim_light.data.color = (1.0, 1.0, 1.0)
    rim_light.rotation_euler = (math.radians(-55), 0, math.radians(180))

    # 8. Broadcast Cinematic Tracking Camera
    bpy.ops.object.camera_add(location=(3.6, -6.8, 2.5))
    cam = bpy.context.active_object
    cam.name = "BroadcastCam"
    cam.data.lens = 45  # 45mm broadcast lens
    cam.rotation_euler = (math.radians(72), 0, math.radians(28))
    bpy.context.scene.camera = cam

    # 9. Render Engine & Output Target
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.device = 'CPU'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'

    abs_output = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)
    scene.render.filepath = abs_output

    print(f"[BlenderService] Executing Cycles render to: {abs_output}")
    bpy.ops.render.render(write_still=True)
    print(f"[BlenderService] Render complete successfully: {abs_output}")


if __name__ == "__main__":
    args = parse_args()
    build_scene(
        play_id=args.play_id,
        drama_index=args.drama_index,
        impact_force=args.impact_force,
        output_path=args.output_path,
        samples=args.samples
    )
