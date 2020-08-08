bl_info = {
    "name": "Cupboard",
    "description": "This addon creates a simple parameterized cupboard.",
    "author": "Karel Vrabec",
    "version": (1, 0, 0),
    "blender": (2, 79, 0), # b
    "location": "View3D > Add > Mesh > Cupboard",
    "wiki_url": "https://gitlab.fit.cvut.cz/BI-PGA/b191/vrabekar",
    "category": "Add Mesh"
}

# ==============================

import bpy

class Cupboard(bpy.types.Operator):
    
    bl_idname = "object.cupboard"
    bl_label = "Cupboard"
    bl_options = {"REGISTER", "UNDO"}
    
    # ==============================
    # GUI
    # ==============================

    options = [
        ("–", "–", "", 4),
        ("DRAWERS", "Drawers", "", 3),
        ("DOORS", "Doors", "", 2),
    ]

    st_cover = bpy.props.EnumProperty(
        name="Cover (FIRST X SHELF):",
        items=options,
        default="DOORS"
    )
    
    nd_cover = bpy.props.EnumProperty(
        name="Cover (SECOND X SHELF):",
        items=options,
        default="DRAWERS"
    )
    
    rd_cover = bpy.props.EnumProperty(
        name="Cover (THIRD X SHELF):",
        items=options,
        default="–"
    )

    sh_x_quantity = bpy.props.IntProperty(
        name="Quantity (X SHELVES):",
        default=2, min=0, max=2, step=1
    )

    sh_y1_quantity = bpy.props.IntProperty(
        name="Quantity (FIRST Y SHELVES):",
        default=4, min=0, max=10, step=1
    )

    sh_y2_quantity = bpy.props.IntProperty(
        name="Quantity (SECOND Y SHELVES):",
        default=3, min=0, max=10, step=1
    )

    sh_y3_quantity = bpy.props.IntProperty(
        name="Quantity (THIRD Y SHELVES):",
        default=2, min=0, max=10, step=1
    )

    cb_size = bpy.props.FloatVectorProperty(
        name="Size (CUPBOARD):",
        subtype="XYZ",
        default=(0.35, 0.9, 1.0), min=0.35
    )

    do_ha_size = bpy.props.FloatVectorProperty(
        name="Size (DOORS HANDLES):",
        subtype="XYZ",
        default=(0.015, 0.02, 0.2), min=0.01
    )

    dr_ha_size = bpy.props.FloatVectorProperty(
        name="Size (DRAWERS HANDLES):",
        subtype="XYZ",
        default=(0.015, 0.1, 0.02), min=0.01
    )

    cb_thickness = bpy.props.FloatProperty(
        name="Thickness (CUPBOARD):",
        default=0.02, min=0.01, max=0.2, step=0.5
    )    

    sh_thickness = bpy.props.FloatProperty(
        name="Thickness (SHELVES):",
        default=0.01, min=0.01, max=0.2, step=0.5
    )

    co_thickness = bpy.props.FloatProperty(
        name="Thickness (COVER):",
        default=0.02, min=0.01, max=0.2, step=0.5
    )

    le_radius = bpy.props.FloatProperty(
        name="Radius (LEGS):",
        default=0.08, min=0.01, step=0.1
    )
    
    le_depth = bpy.props.FloatProperty(
        name="Depth (LEGS):",
        default=0.04, min=0.01, step=0.1
    )
    
    # ==============================
    # Zakladni metody
    # ==============================
    
    def execute(self, context):
        # Vypocte vzdalenost mezi X-ovymi polickami
        sh_x_distance = 2*(self.cb_size[1] - 2*self.cb_thickness - self.sh_x_quantity*self.sh_thickness) / (self.sh_x_quantity + 1)

        # Vypocte vzdalenost mezi Y-ovymi polickami
        sh_y1_distance = 2*(self.cb_size[2] - 2*self.cb_thickness - self.sh_y1_quantity*self.sh_thickness) / (self.sh_y1_quantity + 1)
        sh_y2_distance = 2*(self.cb_size[2] - 2*self.cb_thickness - self.sh_y2_quantity*self.sh_thickness) / (self.sh_y2_quantity + 1)
        sh_y3_distance = 2*(self.cb_size[2] - 2*self.cb_thickness - self.sh_y3_quantity*self.sh_thickness) / (self.sh_y3_quantity + 1)
        
		# Vytvori skrin
        self.create_cupboard(
            self.cb_size,
            self.cb_thickness
        )

        # Vytvori nohy
        self.create_legs(
            self.le_radius,
            self.le_depth,
            self.cb_size
        )

        # Vytvori policky podle osy X
        self.create_x_separators(
            self.cb_size,
            self.cb_thickness,
            self.sh_thickness,
            self.sh_x_quantity,
            sh_x_distance
        )

        # Vytvori policky podle osy Y
        self.create_y_separators(
            self.cb_size,
            self.cb_thickness,
            self.sh_thickness,
            self.sh_x_quantity,
            (self.sh_y1_quantity, self.sh_y2_quantity, self.sh_y3_quantity),
            sh_x_distance,
            (sh_y1_distance, sh_y2_distance, sh_y3_distance)
        )

        # Vytvori dvirka
        self.create_doors(
            self.cb_size,
            self.do_ha_size,
            self.cb_thickness,
            self.sh_thickness,
            self.co_thickness,
            self.sh_x_quantity,
            sh_x_distance,
            (self.st_cover, self.nd_cover, self.rd_cover)
        )

        # Vytvori supliky
        self.create_drawers(
            self.cb_size,
            self.dr_ha_size,
            self.cb_thickness,
            self.sh_thickness,
            self.co_thickness,
            self.sh_x_quantity,
            (self.sh_y1_quantity, self.sh_y2_quantity, self.sh_y3_quantity),
            sh_x_distance,
            (sh_y1_distance, sh_y2_distance, sh_y3_distance),
            (self.st_cover, self.nd_cover, self.rd_cover)
        )
                
        return {"FINISHED"}

    # ==============================

    # Vytvori novou krychli
    def create_cube(self, name, dist_x, dist_y, dist_z, size_x, size_y, size_z):
        bpy.ops.mesh.primitive_cube_add(radius=1, location=(dist_x, dist_y, dist_z))
        bpy.context.scene.objects.active.scale = (size_x, size_y, size_z)
        bpy.context.active_object.name = name

    # ==============================

    # Vytvori novy valec
    def create_cylinder(self, name, radius, depth, x, y, z):
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=(x, y, z))
        bpy.context.active_object.name = name

    # ==============================

    # Provede rozdil dvou objektu
    def make_difference(self, cutted, cutting):
        mod = cutted.modifiers.new(name="Boolean", type="BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.object = cutting
        bpy.context.scene.objects.active = cutted
        bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")

    # ==============================

    def create_cupboard(self, size, thick):
		# Vytvori skrin
        self.create_cube("CUPBOARD", 0.0, 0.0, 1.0, size[0], size[1], size[2])
        cupboard = bpy.context.active_object
 
		# Vytvori krychli k vyrezu vnitrku skrine
        self.create_cube("MIDDLE CUTTER", 0.02, 0.0, 1.0, size[0], size[1] - 2*thick, size[2] - 2*thick)
        m_cube = bpy.context.active_object

		# Vytvori krychli k vyrezu prave strany skrine
        self.create_cube("RIGHT CUTTER", 0.0, size[1], 1.0, size[0]-0.1, 0.01, size[2]-0.1)
        r_cube = bpy.context.active_object

		# Vytvori krychli k vyrezu leve strany skrine
        self.create_cube("LEFT CUTTER", 0.0, -size[1], 1.0, size[0]-0.1, 0.01, size[2]-0.1)
        l_cube = bpy.context.active_object

        # Provede rozdily vsech objektu
        self.make_difference(cupboard, m_cube)
        self.make_difference(cupboard, r_cube)
        self.make_difference(cupboard, l_cube)

        # Odstrani vsechny vyrezove krychle
        bpy.data.objects.remove(m_cube, True)
        bpy.data.objects.remove(r_cube, True)
        bpy.data.objects.remove(l_cube, True)

    # ==============================

    def create_legs(self, radius, depth, cb_size):
        # Vypocte X-ovou pozici
        front = cb_size[0] - cb_size[0]/2
        back = -cb_size[0] + cb_size[0]/2
        
        # Vypocte Y-ovou pozici
        left = -cb_size[1] + cb_size[1]/6
        right = cb_size[1] - cb_size[1]/6
        
        # Vypocte Z-ovou pozici
        z = 1.0 - cb_size[2] - depth/2
        
        # Vytvori nohy
        self.create_cylinder("FRONT RIGHT LEG", radius, depth, front, right, z)
        self.create_cylinder("BACK RIGHT LEG", radius, depth, back, right, z)
        self.create_cylinder("FRONT LEFT LEG", radius, depth, front, left, z)
        self.create_cylinder("BACK LEFT LEG", radius, depth, back, left, z)

    # ==============================

    def create_x_separators(self, cb_size, cb_thick, sh_thick, sh_x_quant, sh_x_dist):
        # Vytvori policky podle osy X
        for i in range(0, sh_x_quant):
            self.create_cube(
                "X SHELF " + str(i), # Nazev
                0.01, -cb_size[1] + 2*cb_thick + sh_x_dist + sh_thick + i*(sh_x_dist + 2*sh_thick), 1.0, # Pozice (X, Y, Z)
                cb_size[0] - 0.01, sh_thick, cb_size[2] - 2*cb_thick # Velikost (X, Y, Z)
            )
            
    # ==============================

    def create_y_separators(self, cb_size, cb_thick, sh_thick, sh_x_quant, sh_y_quant, sh_x_dist, sh_y_dist):
        # Vytvori policky podle osy Y
        for i in range(0, sh_x_quant+1):
            for j in range(0, sh_y_quant[i]):
                self.create_cube(
                    "Y SHELF " + str(i) + " " + str(j), # Nazev
                    0.0, # Pozice (X)
                    -cb_size[1] + 2*cb_thick + sh_x_dist/2 + i*(sh_x_dist + 2*sh_thick), # Pozice (Y)
                    1.0 - cb_size[2] + 2*cb_thick + sh_y_dist[i] + sh_thick + j*(sh_y_dist[i] + 2*sh_thick), # Pozice (Z)
                    cb_size[0] - 0.02, sh_x_dist/2, sh_thick # Velikost (X, Y, Z)
                )

    # ==============================

    def create_doors(self, cb_size, do_ha_size, cb_thick, sh_thick, co_thick, sh_x_quant, sh_x_dist, covers):
        for i in range(0, sh_x_quant+1):
            if (covers[i] != "DOORS"):
                continue
            
            # Rukojet prvnich dveri umisti doprava
            if not i:
                coefficient = 5/6
            else:
                coefficient = 1/6

            # Vytvori dvirka
            self.create_cube(
                "DOORS " + str(i), # Nazev
                cb_size[0] + co_thick, -cb_size[1] + 2*cb_thick + sh_x_dist/2 + i*(sh_x_dist + 2*sh_thick), 1.0, # Pozice (X, Y, Z)
                co_thick, sh_x_dist/2, cb_size[2] - 2*cb_thick # Velikost (X, Y, Z)
            )
            
            # Vytvori rukojet
            self.create_cube(
                "DOORS HANDLE " + str(i), # Nazev
                cb_size[0] + 2*co_thick + do_ha_size[0], -cb_size[1] + 2*cb_thick + sh_x_dist*coefficient + i*(sh_x_dist + 2*sh_thick), 1.0, # Pozice (X, Y, Z)
                do_ha_size[0], do_ha_size[1], do_ha_size[2] # Velikost (X, Y, Z)
            )

    # ==============================

    def create_drawers(self, cb_size, dr_ha_size, cb_thick, sh_thick, co_thick, sh_x_quant, sh_y_quant, sh_x_dist, sh_y_dist, covers):
        for i in range(0, sh_x_quant+1):
            if (covers[i] != "DRAWERS"):
                continue
            
            for j in range(0, sh_y_quant[i]+1):
                # Vytvori suplik
                self.create_cube(
                    "DRAWER " + str(i) + " " + str(j), # Nazev
                    cb_size[0] + co_thick, # Pozice (X)
                    -cb_size[1] + 2*cb_thick + sh_x_dist/2 + i*(sh_x_dist + 2*sh_thick), # Pozice (Y)
                    1.0 - cb_size[2] + 2*cb_thick + sh_y_dist[i]/2 + j*(sh_y_dist[i] + 2*sh_thick), # Pozice (Z)
                    co_thick, sh_x_dist/2, sh_y_dist[i]/2 # Velikost (X, Y, Z)
                )
                
                # Vytvori rukojet
                self.create_cube(
                    "DRAWER HANDLE " + str(i) + " " + str(j), # Nazev
                    cb_size[0] + 2*co_thick + dr_ha_size[0], # Pozice (X)
                    -cb_size[1] + 2*cb_thick + sh_x_dist/2 + i*(sh_x_dist + 2*sh_thick), # Pozice (Y)
                    1.0 - cb_size[2] + 2*cb_thick + sh_y_dist[i]/2 + j*(sh_y_dist[i] + 2*sh_thick), # Pozice (Z)
                    dr_ha_size[0], dr_ha_size[1], dr_ha_size[2] # Velikost (X, Y, Z)
                )

# ==============================

def cb_item(self, context):
    self.layout.operator(Cupboard.bl_idname, icon="COLLAPSEMENU")

def register():
    bpy.utils.register_class(Cupboard)
    bpy.types.INFO_MT_mesh_add.append(cb_item)

def unregister():
    bpy.utils.unregister_class(Cupboard)
    bpy.types.INFO_MT_mesh_add.remove(cb_item)

if __name__ == "__main__":
    register()
