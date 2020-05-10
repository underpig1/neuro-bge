import bpy
import nodeitems_utils
import mathutils
import functools
import math
import bpy_extras
import os
import aud
from bpy.app.handlers import persistent

class LogicEditor(bpy.types.NodeTree):
    bl_idname = "LogicEditor"
    bl_label = "Logic Editor"
    bl_icon = "BLENDER"

#class GameView(bpy.types.ViewLayer):
#    bl_idname = "GameView"
#    bl_label = "Game View"
#    bl_icon = "BLENDER"

class LogicNode(bpy.types.Node):
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "LogicEditor"

class OnKeyEvent(LogicNode):
    bl_idname = "OnKeyEvent"
    bl_label = "On Key"
    bl_icon = "PLUS"
    continuousUpdate = True
    key = bpy.props.EnumProperty(
        name = "Key",
        items = (("1", "A", "A Key"), ("2", "B", "B Key"), ("3", "C", "C Key"), ("4", "D", "D Key"), ("5", "E", "E Key"), ("6", "F", "F Key"), ("7", "G", "G Key"), ("8", "H", "H Key"), ("9", "I", "I Key"), ("10", "J", "J Key"), ("11", "K", "K Key"), ("12", "L", "L Key"), ("13", "M", "M Key"), ("14", "N", "N Key"), ("15", "O", "O Key"), ("16", "P", "P Key"), ("17", "Q", "Q Key"), ("18", "R", "R Key"), ("19", "S", "S Key"), ("20", "T", "T Key"), ("21", "U", "U Key"), ("22", "V", "V Key"), ("23", "W", "W Key"), ("24", "X", "X Key"), ("25", "Y", "Y Key"), ("26", "Z", "Z Key"), ("27", "0", "0 Key"), ("28", "1", "1 Key"), ("29", "2", "2 Key"), ("30", "3", "3 Key"), ("31", "4", "4 Key"), ("32", "5", "5 Key"), ("33", "6", "6 Key"), ("34", "7", "7 Key"), ("35", "8", "8 Key"), ("36", "9", "9 Key"))
    )

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def draw_buttons(self, context, layout):
        layout.prop(self, "key", text = "")

    def runScript(self):
        runScript(self)

    def updateNode(self):
        if str(bpy.types.WindowManager.event.type) == str(chr(ord("@") + int(self.key))) and bpy.types.WindowManager.event.value == "PRESS":
            self.runScript()

class OnClickEvent(LogicNode):
    bl_idname = "OnClickEvent"
    bl_label = "On Click"
    bl_icon = "PLUS"
    continuousUpdate = True

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def runScript(self):
        runScript(self)

    def updateNode(self):
        if str(bpy.types.WindowManager.event.type) == "LEFTMOUSE" and bpy.types.WindowManager.event.value == "PRESS":
            self.runScript()

class OnInteractionEvent(LogicNode):
    bl_idname = "OnInteractionEvent"
    bl_label = "On Interaction"
    bl_icon = "PLUS"
    continuousUpdate = True

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")
        self.outputs.new("NodeSocketBool", "Interaction")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def runScript(self):
        runScript(self)

    def updateNode(self):
        if bpy.types.WindowManager.run:
            if "object" in self:
                object = self["object"]
            else:
                output = self
                while output.bl_idname != "Output":
                    node = output
                    for outputs in node.outputs:
                        for links in outputs.links:
                            output = links.to_node
                try:
                    object = output["object"]
                except KeyError:
                    report("Output does not contain object assignment")
            for obj in bpy.context.scene.objects:
                if obj.type == "MESH" and collision(object, obj) and obj != object:
                    self.runScript()
                    for link in self.outputs[1].links:
                        link.to_node["objective"] = obj

class Output(LogicNode):
    bl_idname = "Output"
    bl_label = "Output"
    bl_icon = "BLENDER"

    def init(self, context):
        self.inputs.new("NodeSocketShader", "Script")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def runScript(self):
        pass

class ActionNode(LogicNode):
    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")
        self.inputs.new("NodeSocketShader", "Script")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

class InputNode(LogicNode):
    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def callConnected(self):
        self.retrieveValues()
        for output in self.outputs:
            for link in output.links:
                if hasattr(link.to_node, "nodeType"):
                    if link.to_node.nodeType == "InputNode":
                        link.to_node.callConnected()
                for i in range(len(self.outputs)):
                    for j in range(len(self.outputs[i].links)):
                        self.outputs[i].links[j].to_socket.default_value = self.outputs[i].default_value

class ObjectPositionInput(InputNode):
    bl_idname = "ObjectPositionInput"
    bl_label = "Object Position"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.outputs.new("NodeSocketVector", "Vector")

    def retrieveValues(self):
        self.outputs[0].default_value = runScript(self).location

class ObjectRotationInput(InputNode):
    bl_idname = "ObjectRotationInput"
    bl_label = "Object Rotation"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.outputs.new("NodeSocketVector", "Vector")

    def retrieveValues(self):
        rotation = runScript(self).rotation_euler
        self.outputs[0].default_value = mathutils.Vector((math.degrees(rotation[0]), math.degrees(rotation[1]), math.degrees(rotation[2])))

class ObjectScaleInput(InputNode):
    bl_idname = "ObjectScaleInput"
    bl_label = "Object Scale"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.outputs.new("NodeSocketVector", "Vector")

    def retrieveValues(self):
        self.outputs[0].default_value = runScript(self).scale

class MouseInput(InputNode):
    bl_idname = "MouseInput"
    bl_label = "Mouse"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    continuousUpdate = True

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.outputs.new("NodeSocketFloat", "X")
        self.outputs.new("NodeSocketFloat", "Y")
        self.outputs.new("NodeSocketBool", "Click")

    def retrieveValues(self):
        self.outputs[0].default_value = bpy.types.WindowManager.mouse[0]
        self.outputs[1].default_value = bpy.types.WindowManager.mouse[1]
        if str(bpy.types.WindowManager.event.type) == "LEFTMOUSE" and bpy.types.WindowManager.event.value == "PRESS":
            self.outputs[2].default_value = True
        else:
            self.outputs[2].default_value = False

    def updateNode(self):
        self.retrieveValues()

class GravityInput(InputNode):
    bl_idname = "GravityInput"
    bl_label = "Gravity"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.outputs.new("NodeSocketVector", "Vector")

    def retrieveValues(self):
        self.outputs[0].default_value = bpy.context.scene.gravity

class CustomPropertyInput(InputNode):
    bl_idname = "CustomPropertyInput"
    bl_label = "Custom Property"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketString", "Property")
        self.outputs.new("NodeSocketFloat", "Value")

    def retrieveValues(self):
        self.outputs[0].default_value = runScript(self)[self.inputs[1].default_value]

class MathInput(InputNode):
    bl_idname = "MathInput"
    bl_label = "Math"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    operator = bpy.props.EnumProperty(
        name = "Operator",
        items = (("1", "Add", "Addition operator"), ("2", "Subtract", "Subtraction operator"), ("3", "Multiply", "Multiplication operator"), ("4", "Divide", "Division operator"), ("5", "Min", "Minimum operator"), ("6", "Max", "Maximum operator"), ("7", "Power", "Exponent operator"), ("8", "Modulo", "Modulo operator"), ("9", "Square Root", "Square root operator"), ("10", "Root", "Root operator"), ("11", "Cosine", "Cosine operator"), ("12", "Sine", "Sine operator"), ("13", "Tangent", "Tangent operator"), ("14", "Floor", "Floor operator"), ("15", "Ceiling", "Ceiling operator"), ("16", "Round", "Round operator"), ("17", "Arc Cosine", "Arc cosine operator"), ("18", "Arc Sine", "Arc sine operator"), ("19", "Arc Tangent", "Arc tangent operator"), ("20", "Remainder", "Remainder operator"))
    )

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketFloat", "Value")
        self.inputs.new("NodeSocketFloat", "Value")
        self.outputs.new("NodeSocketFloat", "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text = "")

    def retrieveValues(self):
        values = [float(self.inputs[1].default_value), float(self.inputs[2].default_value)]
        if int(self.operator) == 1:
            self.outputs[0].default_value = values[0] + values[1]
        elif int(self.operator) == 2:
            self.outputs[0].default_value = values[0] - values[1]
        elif int(self.operator) == 3:
            self.outputs[0].default_value = values[0] * values[1]
        elif int(self.operator) == 4:
            self.outputs[0].default_value = values[0] / values[1]
        elif int(self.operator) == 5:
            self.outputs[0].default_value = min(values[0], values[1])
        elif int(self.operator) == 6:
            self.outputs[0].default_value = max(values[0], values[1])
        elif int(self.operator) == 7:
            self.outputs[0].default_value = values[0] ** values[1]
        elif int(self.operator) == 8:
            self.outputs[0].default_value = values[0] % values[1]
        elif int(self.operator) == 9:
            self.outputs[0].default_value = math.sqrt(values[0])
        elif int(self.operator) == 10:
            self.outputs[0].default_value = values[0] ** (1.0/values[1])
        elif int(self.operator) == 11:
            self.outputs[0].default_value = math.cos(values[0])
        elif int(self.operator) == 12:
            self.outputs[0].default_value = math.sin(values[0])
        elif int(self.operator) == 13:
            self.outputs[0].default_value = math.tan(values[0])
        elif int(self.operator) == 14:
            self.outputs[0].default_value = float(math.floor(values[0]))
        elif int(self.operator) == 15:
            self.outputs[0].default_value = float(math.ceil(values[0]))
        elif int(self.operator) == 16:
            self.outputs[0].default_value = float(math.round(values[0]))
        elif int(self.operator) == 17:
            self.outputs[0].default_value = math.acos(values[0])
        elif int(self.operator) == 18:
            self.outputs[0].default_value = math.asin(values[0])
        elif int(self.operator) == 19:
            self.outputs[0].default_value = math.atan(values[0])
        elif int(self.operator) == 20:
            self.outputs[0].default_value = math.remainder(values[0], values[1])

class ComparisonLogic(InputNode):
    bl_idname = "ComparisonLogic"
    bl_label = "Comparison"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    operator = bpy.props.EnumProperty(
        name = "Operator",
        items = (("1", "Greater Than", "Greater than"), ("2", "Less Than", "Less than"), ("3", "Greater Than Or Equal To", "Greater than or equal to"), ("4", "Less Than Or Equal To", "Less than or equal to"), ("5", "Equal To", "Equal to"), ("6", "Not Equal To", "Not equal to"))
    )

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketFloat", "Value")
        self.inputs.new("NodeSocketFloat", "Value")
        self.outputs.new("NodeSocketBool", "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text = "")

    def retrieveValues(self):
        values = [float(self.inputs[1].default_value), float(self.inputs[2].default_value)]
        if int(self.operator) == 1:
            self.outputs[0].default_value = values[0] > values[1]
        elif int(self.operator) == 2:
            self.outputs[0].default_value = values[0] < values[1]
        elif int(self.operator) == 3:
            self.outputs[0].default_value = values[0] >= values[1]
        elif int(self.operator) == 4:
            self.outputs[0].default_value = values[0] <= values[1]
        elif int(self.operator) == 5:
            self.outputs[0].default_value = values[0] == values[1]
        elif int(self.operator) == 6:
            self.outputs[0].default_value = values[0] != values[1]

class GateLogic(InputNode):
    bl_idname = "GateLogic"
    bl_label = "Gate"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    operator = bpy.props.EnumProperty(
        name = "Operator",
        items = (("1", "And", "And gate"), ("2", "Or", "Or gate"), ("3", "Not", "Not gate"),  ("4", "Not And", "Not and gate"), ("5", "Not Or", "Not or gate"))
    )

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketBool", "Value")
        self.inputs.new("NodeSocketBool", "Value")
        self.outputs.new("NodeSocketBool", "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text = "")

    def retrieveValues(self):
        values = [float(self.inputs[1].default_value), float(self.inputs[2].default_value)]
        if int(self.operator) == 1:
            self.outputs[0].default_value = values[0] and values[1]
        elif int(self.operator) == 2:
            self.outputs[0].default_value = values[0] or values[1]
        elif int(self.operator) == 3:
            self.outputs[0].default_value = not values[0]
        elif int(self.operator) == 4:
            self.outputs[0].default_value = (not values[0]) and (not values[1])
        elif int(self.operator) == 5:
            self.outputs[0].default_value = (not values[0]) or (not values[1])

class SeperateVectorInput(InputNode):
    bl_idname = "SeperateVectorInput"
    bl_label = "Seperate Vector"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketVector", "Vector")
        self.outputs.new("NodeSocketFloat", "X")
        self.outputs.new("NodeSocketFloat", "Y")
        self.outputs.new("NodeSocketFloat", "Z")

    def retrieveValues(self):
        value = mathutils.Vector(tuple(self.inputs[1].default_value))
        self.outputs[0].default_value = value[0]
        self.outputs[1].default_value = value[1]
        self.outputs[2].default_value = value[2]

class CombineVectorInput(InputNode):
    bl_idname = "CombineVectorInput"
    bl_label = "Combine Vector"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.outputs.new("NodeSocketVector", "Vector")
        self.inputs.new("NodeSocketFloat", "X")
        self.inputs.new("NodeSocketFloat", "Y")
        self.inputs.new("NodeSocketFloat", "Z")

    def retrieveValues(self):
        self.outputs[0].default_value = mathutils.Vector((float(self.inputs[1].default_value), float(self.inputs[2].default_value), float(self.inputs[3].default_value)))

class VectorMathInput(InputNode):
    bl_idname = "VectorMathInput"
    bl_label = "Vector Math"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    operator = bpy.props.EnumProperty(
        name = "Operator",
        items = (("1", "Add", "Addition operator"), ("2", "Subtract", "Subtraction operator"), ("3", "Multiply", "Multiplication operator"), ("4", "Divide", "Division operator"), ("5", "Min", "Minimum operator"), ("6", "Max", "Maximum operator"), ("7", "Power", "Exponent operator"), ("8", "Modulo", "Modulo operator"))
    )

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketVector", "Vector")
        self.inputs.new("NodeSocketVector", "Vector")
        self.outputs.new("NodeSocketVector", "Vector")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text = "")

    def retrieveValues(self):
        values = [mathutils.Vector(tuple(self.inputs[1].default_value)), mathutils.Vector(tuple(self.inputs[2].default_value))]
        if int(self.operator) == 1:
            self.outputs[0].default_value = values[0] + values[1]
        elif int(self.operator) == 2:
            self.outputs[0].default_value = values[0] - values[1]
        elif int(self.operator) == 3:
            self.outputs[0].default_value = values[0] * values[1]
        elif int(self.operator) == 4:
            self.outputs[0].default_value = values[0] / values[1]
        elif int(self.operator) == 5:
            self.outputs[0].default_value = min(values[0], values[1])
        elif int(self.operator) == 6:
            self.outputs[0].default_value = max(values[0], values[1])
        elif int(self.operator) == 5:
            self.outputs[0].default_value = max(values[0], values[1])
        elif int(self.operator) == 7:
            self.outputs[0].default_value = values[0] ** values[1]
        elif int(self.operator) == 8:
            self.outputs[0].default_value = values[0] % values[1]

class VectorTransformInput(InputNode):
    bl_idname = "VectorTransformInput"
    bl_label = "Vector Transform"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    operator = bpy.props.EnumProperty(
        name = "Operator",
        items = (("1", "Multiply", "Multiplication operator"), ("2", "Divide", "Division operator"))
    )

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketVector", "Vector")
        self.inputs.new("NodeSocketFloat", "Value")
        self.outputs.new("NodeSocketVector", "Vector")

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text = "")

    def retrieveValues(self):
        values = [mathutils.Vector(tuple(self.inputs[1].default_value)), float(self.inputs[2].default_value)]
        if int(self.operator) == 1:
            self.outputs[0].default_value = values[0] * values[1]
        elif int(self.operator) == 2:
            self.outputs[0].default_value = values[0] / values[1]

class DistanceInput(InputNode):
    bl_idname = "DistanceInput"
    bl_label = "Distance"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketVector", "Vector")
        self.inputs.new("NodeSocketVector", "Vector")
        self.outputs.new("NodeSocketFloat", "Distance")

    def retrieveValues(self):
        values = [tuple(self.inputs[0].default_value), tuple(self.inputs[1].default_value)]
        self.outputs[0].default_value = math.sqrt((values[0][0] - values[1][0])**2 + (values[0][1] - values[1][1])**2 + (values[0][2] - values[1][2])**2)

class ObjectiveInput(InputNode):
    bl_idname = "ObjectiveInput"
    bl_label = "Objective"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    continuousUpdate = True
    objective = bpy.props.StringProperty()

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "objective", bpy.data, "objects", text = "")

    def init(self, context):
        self.outputs.new("NodeSocketBool", "Object")

    def retrieveValues(self):
        self["object"] = bpy.data.objects[str(self.objective)]
        for link in self.outputs[0].links:
            link.to_node["objective"] = runScript(self)

    def updateNode(self):
        self.retrieveValues()

class InteractionInput(InputNode):
    bl_idname = "InteractionInput"
    bl_label = "Interaction"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Realtime")
        self.inputs.new("NodeSocketBool", "Object")
        self.outputs.new("NodeSocketBool", "Interaction")

    def retrieveValues(self):
        object = runScript(self)
        objective = self["objective"]
        self.outputs[0].default_value = collision(object, objective)

def populateVariables(context, layout):
    items = []
    for key in list(bpy.types.Object.variables.keys()):
        items.append((key, key, key))
    return items

class VariableInput(InputNode):
    bl_idname = "VariableInput"
    bl_label = "Variable"
    bl_icon = "PLUS"
    nodeType = "InputNode"
    variable = bpy.props.EnumProperty(name = "Variable", items = populateVariables)

    def init(self, context):
        self.outputs.new("NodeSocketFloat", "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "variable", text = "")

    def retrieveValues(self):
        self.outputs[0].default_value = bpy.types.Object.variables[self.variable]

class DegreesToRadiansInput(InputNode):
    bl_idname = "DegreesToRadiansInput"
    bl_label = "Degrees To Radians"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Value")
        self.outputs.new("NodeSocketFloat", "Value")

    def retrieveValues(self):
        self.outputs[0].default_value = math.radians(self.inputs[0].default_value)

class RadiansToDegreesInput(InputNode):
    bl_idname = "RadiansToDegreesInput"
    bl_label = "Radians To Degrees"
    bl_icon = "PLUS"
    nodeType = "InputNode"

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Value")
        self.outputs.new("NodeSocketFloat", "Value")

    def retrieveValues(self):
        self.outputs[0].default_value = math.degrees(self.inputs[0].default_value)

class SetVariableAction(ActionNode):
    bl_idname = "SetVariableAction"
    bl_label = "Set Variable"
    bl_icon = "PLUS"
    variable = bpy.props.EnumProperty(name = "Variable", items = populateVariables)

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Value")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "variable", text = "")

    def runScript(self):
        bpy.types.Object.variables[self.variable] = float(self.inputs[0].default_value)
        runScript(self)

class ScriptAction(ActionNode):
    bl_idname = "ScriptAction"
    bl_label = "Script"
    bl_icon = "PLUS"
    script = bpy.props.StringProperty()

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "script", bpy.data, "texts", text = "")

    def runScript(self):
        #text = bpy.data.texts.load(str(self.script))
        text = bpy.data.texts[str(self.script)]
        context = bpy.context.copy()
        context["edit_text"] = text
        bpy.ops.text.run_script(context)
        runScript(self)

class MoveAction(ActionNode):
    bl_idname = "MoveAction"
    bl_label = "Move"
    bl_icon = "PLUS"
    bl_width_default = 250

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Local")
        self.inputs.new("NodeSocketVector", "Vector")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        vector = mathutils.Matrix.Translation(tuple(self.inputs[1].default_value))
        if self.inputs[0].default_value:
            object.matrix_basis @= vector
        else:
            object.location.x += list(self.inputs[1].default_value)[0]
            object.location.y += list(self.inputs[1].default_value)[1]
            object.location.z += list(self.inputs[1].default_value)[2]

class RotateAction(ActionNode):
    bl_idname = "RotateAction"
    bl_label = "Rotate"
    bl_icon = "PLUS"
    bl_width_default = 250

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Local")
        self.inputs.new("NodeSocketVector", "Vector")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        if self.inputs[0].default_value:
            object.rotation_euler.rotate_axis("X", math.radians(list(self.inputs[1].default_value)[0]))
            object.rotation_euler.rotate_axis("Y", math.radians(list(self.inputs[1].default_value)[1]))
            object.rotation_euler.rotate_axis("Z", math.radians(list(self.inputs[1].default_value)[2]))
        else:
            object.rotation_euler.x += math.radians(list(self.inputs[1].default_value)[0])
            object.rotation_euler.y += math.radians(list(self.inputs[1].default_value)[1])
            object.rotation_euler.z += math.radians(list(self.inputs[1].default_value)[2])

class ScaleAction(ActionNode):
    bl_idname = "ScaleAction"
    bl_label = "Scale"
    bl_icon = "PLUS"
    bl_width_default = 250

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Local")
        self.inputs.new("NodeSocketVector", "Vector")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        object.scale.x += list(self.inputs[1].default_value)[0]
        object.scale.y += list(self.inputs[1].default_value)[1]
        object.scale.z += list(self.inputs[1].default_value)[2]

class SetTransformAction(ActionNode):
    bl_idname = "SetTransformAction"
    bl_label = "Set Transform"
    bl_icon = "PLUS"
    bl_width_default = 250

    def init(self, context):
        self.inputs.new("NodeSocketVector", "Position")
        self.inputs.new("NodeSocketVector", "Rotation")
        self.inputs.new("NodeSocketVector", "Scale")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        object.location.x = list(self.inputs[0].default_value)[0]
        object.location.y = list(self.inputs[0].default_value)[1]
        object.location.z = list(self.inputs[0].default_value)[2]
        object.rotation_euler.x = math.radians(list(self.inputs[1].default_value)[0])
        object.rotation_euler.y = math.radians(list(self.inputs[1].default_value)[1])
        object.rotation_euler.z = math.radians(list(self.inputs[1].default_value)[2])
        object.scale.x = list(self.inputs[2].default_value)[0]
        object.scale.y = list(self.inputs[2].default_value)[1]
        object.scale.z = list(self.inputs[2].default_value)[2]

class ParentAction(ActionNode):
    bl_idname = "ParentAction"
    bl_label = "Parent"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Object")
        self.inputs.new("NodeSocketBool", "Maintain Relative Position")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        objective = self["objective"]
        object.parent = objective
        if self.inputs[1].default_value:
            object.matrix_parent_inverse = objective.matrix_world.inverted()

class RemoveParentAction(ActionNode):
    bl_idname = "RemoveParentAction"
    bl_label = "Remove Parent"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Maintain Relative Position")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        matrix = object.matrix_world.copy()
        object.parent = None
        if self.inputs[0].default_value:
            object.matrix_world = matrix

class DelayAction(ActionNode):
    bl_idname = "DelayAction"
    bl_label = "Delay"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Delay")
        super().init(context)

    def loop(self):
        if bpy.types.WindowManager.run:
            runScript(self)

    def runScript(self):
        bpy.app.timers.register(self.loop, first_interval = self.inputs[0].default_value)

class MergeScriptAction(ActionNode):
    bl_idname = "MergeScriptAction"
    bl_label = "Merge Script"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketShader", "Script")
        super().init(context)

    def runScript(self):
        pass

class VisibilityAction(ActionNode):
    bl_idname = "VisibilityAction"
    bl_label = "Visibility"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Appear")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        if self.inputs[0].default_value:
            if "scale" in self:
                object.scale = self["scale"]
        else:
            self["scale"] = object.scale
            object.scale = mathutils.Vector((0, 0, 0))

class SetGravityAction(ActionNode):
    bl_idname = "SetGravityAction"
    bl_label = "Set Gravity"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketVector", "Vector")
        super().init(context)

    def runScript(self):
        bpy.context.scene.gravity = mathutils.Vector(tuple(self.inputs[0].default_value))

class SetCustomPropertyAction(ActionNode):
    bl_idname = "SetCustomPropertyAction"
    bl_label = "Set Custom Property"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketString", "Property")
        self.inputs.new("NodeSocketFloat", "Value")
        super().init(context)

    def runScript(self):
        runScript(self)[self.inputs[0].default_value] = float(self.inputs[1].default_value)

class PointAtAction(ActionNode):
    bl_idname = "PointAtAction"
    bl_label = "Point At"
    bl_icon = "PLUS"
    bl_width_default = 250

    def init(self, context):
        self.inputs.new("NodeSocketVector", "Point")
        super().init(context)

    def runScript(self):
        object = runScript(self)
        direction = mathutils.Vector(tuple(self.inputs[0].default_value)) - object.matrix_world.to_translation()
        rotation = direction.to_track_quat("X", "Z")
        object.rotation_euler = rotation.to_euler()

class PlayerController(ActionNode):
    bl_idname = "PlayerController"
    bl_label = "Player Controller"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Skewed")
        self.inputs.new("NodeSocketFloat", "Speed")
        self.inputs.new("NodeSocketFloat", "Damping")
        super().init(context)

    def loop(self):
        if bpy.types.WindowManager.run:
            object = runScript(self)
            speed = self.inputs[1].default_value
            damping = 1 / self.inputs[2].default_value
            self["velocity"][0] *= damping
            self["velocity"][1] *= damping
            if str(bpy.types.WindowManager.event.type) == "W" and bpy.types.WindowManager.event.value == "PRESS":
                self["velocity"][0] += speed
            elif str(bpy.types.WindowManager.event.type) == "A" and bpy.types.WindowManager.event.value == "PRESS":
                self["velocity"][1] -= speed
            elif str(bpy.types.WindowManager.event.type) == "S" and bpy.types.WindowManager.event.value == "PRESS":
                self["velocity"][0] -= speed
            elif str(bpy.types.WindowManager.event.type) == "D" and bpy.types.WindowManager.event.value == "PRESS":
                self["velocity"][1] += speed
            if self.inputs[0].default_value:
                object.rotation_euler.z -= math.radians(self["velocity"][1]) * 10
                object.matrix_basis @= mathutils.Matrix.Translation((0, self["velocity"][0], 0))
            else:
                object.matrix_basis @= mathutils.Matrix.Translation(self["velocity"])
            bpy.app.timers.register(self.loop, first_interval = 0.01)

    def runScript(self):
        self["velocity"] = mathutils.Vector((0, 0, 0))
        bpy.app.timers.register(self.loop, first_interval = 0.01)
        runScript(self)

class UIController(ActionNode):
    bl_idname = "UIController"
    bl_label = "UI Controller"
    bl_icon = "PLUS"
    type = bpy.props.EnumProperty(
        name = "Type",
        items = (("1", "Gauge", "Gauge controller"), ("2", "Meter", "Meter controller"))
    )

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Value")
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "type", text = "")

    def loop(self):
        if bpy.types.WindowManager.run:
            object = runScript(self)
            value = float(self.inputs[0].default_value)
            if int(self.type) == 1:
                object.location.z = self["value"][0][2] + value
            elif int(self.type) == 2:
                object.rotation_euler.z = self["value"][1][2] + math.radians(value)
            bpy.app.timers.register(self.loop, first_interval = 0.01)

    def runScript(self):
        object = runScript(self)
        self["value"] = (object.location, object.rotation_euler)
        bpy.app.timers.register(self.loop, first_interval = 0.01)
        runScript(self)

class SceneController(ActionNode):
    bl_idname = "SceneController"
    bl_label = "Scene Controller"
    bl_icon = "PLUS"
    scene = bpy.props.StringProperty()

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "scene", bpy.data, "scenes", text = "")

    def runScript(self):
        bpy.context.window.scene = bpy.data.scenes[str(self.scene)]
        runScript(self)

class AudioController(ActionNode):
    bl_idname = "AudioController"
    bl_label = "Audio Controller"
    bl_icon = "PLUS"
    audio = bpy.props.StringProperty()

    def init(self, context):
        super().init(context)

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "audio", bpy.data, "sounds", text = "")

    def runScript(self):
        device = aud.Device()
        sound = aud.Sound(bpy.data.sounds[str(self.audio)].filepath)
        handle = device.play(sound)

# XR; build; animation; render; curves; ui; tags; property keyframe; restore; button

#    def update(self):
#        print(1)
#        self.local = self.inputs[0]
#        if self.inputs[0]:
#            self.local = self.inputs[1].default_value
#        if self.inputs[1].links[0]:
#            self.loc = self.inputs[1].links[0].from_node.outputs[0].default_value
#        else:
#            self.local = self.inputs[0].default_value


#def stopPlayback(scene):
#    if scene.frame_current == 30:
#        bpy.ops.screen.animation_cancel(restore_frame = False)
#
#bpy.app.handlers.frame_change_pre.append(stopPlayback)
#bpy.ops.screen.animation_play()

class OnRunEvent(LogicNode):
    bl_idname = "OnRunEvent"
    bl_label = "On Run"
    bl_icon = "PLUS"

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def runScript(self):
        print("OnRunEvent")
        runScript(self)

class RepeatLoop(LogicNode):
    bl_idname = "RepeatLoop"
    bl_label = "Repeat"
    bl_icon = "PLUS"

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")
        self.inputs.new("NodeSocketShader", "Script")
        self.outputs.new("NodeSocketShader", "End")
        self.inputs.new("NodeSocketInt", "Repeat")
        self.inputs.new("NodeSocketFloat", "Relief")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def loop(self):
        if bpy.types.WindowManager.run:
            runScript(self)

    def runScript(self):
        for i in range(self.inputs[1].default_value):
            bpy.app.timers.register(self.loop, first_interval = self.inputs[2].default_value*i)
        if bpy.types.WindowManager.run:
            runScript(self, "End")

class RepeatUntilLoop(LogicNode):
    bl_idname = "RepeatUntilLoop"
    bl_label = "Repeat Until"
    bl_icon = "PLUS"

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")
        self.inputs.new("NodeSocketShader", "Script")
        self.outputs.new("NodeSocketShader", "End")
        self.inputs.new("NodeSocketBool", "Condition")
        self.inputs.new("NodeSocketFloat", "Relief")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def loop(self):
        if bpy.types.WindowManager.run:
            if self.inputs[1].default_value:
                runScript(self, "End")
            else:
                runScript(self)
                bpy.app.timers.register(self.loop, first_interval = self.inputs[2].default_value)

    def runScript(self):
        bpy.app.timers.register(self.loop, first_interval = self.inputs[2].default_value)
        runScript(self)

class WhileLoop(LogicNode):
    bl_idname = "WhileLoop"
    bl_label = "While"
    bl_icon = "PLUS"

    def init(self, context):
        self.outputs.new("NodeSocketShader", "Script")
        self.inputs.new("NodeSocketShader", "Script")
        self.outputs.new("NodeSocketShader", "End")
        self.inputs.new("NodeSocketBool", "Condition")
        self.inputs.new("NodeSocketFloat", "Relief")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def loop(self):
        if bpy.types.WindowManager.run:
            if self.inputs[1].default_value:
                runScript(self)
                bpy.app.timers.register(self.loop, first_interval = self.inputs[2].default_value)
            else:
                runScript(self, "End")

    def runScript(self):
        bpy.app.timers.register(self.loop, first_interval = self.inputs[2].default_value)
        runScript(self)

class ModeratorLogic(LogicNode):
    bl_idname = "ModeratorLogic"
    bl_label = "Moderator"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketShader", "Script")
        self.outputs.new("NodeSocketShader", "1st")
        self.outputs.new("NodeSocketShader", "2nd")
        self.inputs.new("NodeSocketFloat", "Relief")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def loop(self):
        if bpy.types.WindowManager.run:
            runScript(self, "2nd")

    def runScript(self):
        runScript(self, "1st")
        bpy.app.timers.register(self.loop, first_interval = self.inputs[1].default_value)

class IfLogic(LogicNode):
    bl_idname = "IfLogic"
    bl_label = "If"
    bl_icon = "PLUS"

    def init(self, context):
        self.inputs.new("NodeSocketBool", "Condition")
        self.outputs.new("NodeSocketShader", "Script")
        self.inputs.new("NodeSocketShader", "Script")
        self.outputs.new("NodeSocketShader", "Else")

    def copy(self, node):
        print("Copied node", node)

    def free(self):
        print("Node removed", self)

    def loop(self):
        runScript(self)

    def runScript(self):
        if self.inputs[0].default_value:
            runScript(self)
        else:
            runScript(self, "Else")

class NodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "LogicEditor"

class RunOperator(bpy.types.Operator):
    bl_idname = "wm.run"
    bl_label = "Run"
    bl_description = "Run all"

    def execute(self, context):
        global keymaps
        bpy.types.WindowManager.run = True
        try:
            for nodeTree in bpy.data.node_groups:
                for node in nodeTree.nodes:
                    if node.bl_idname == "OnRunEvent":
                        node.runScript()
                    elif hasattr(node, "nodeType"):
                        if node.nodeType == "InputNode":
                            #node.retrieveValues()
                            #for i in range(len(node.outputs)):
                            #    node.outputs[i].links[0].to_socket.default_value = node.outputs[i].default_value
                            for input in node.inputs:
                                if len(input.links) == 0:
                                    node.callConnected()
                                    for i in range(len(node.outputs)):
                                        for j in range(len(node.outputs[i].links)):
                                            node.outputs[i].links[j].to_socket.default_value = node.outputs[i].default_value
            bpy.context.scene.frame_end = 1048574
            bpy.ops.screen.animation_play()
            bpy.ops.object.select_all(action = "DESELECT")
            try:
                area = next(area for area in bpy.context.screen.areas if area.type == "VIEW_3D")
                area.spaces[0].region_3d.view_perspective = "CAMERA"
                area.spaces[0].overlay.show_overlays = False
                area.spaces[0].show_gizmo = False
                area.spaces[0].show_region_header = False
                area.spaces[0].shading.type = "RENDERED"
            except StopIteration:
                pass
        except StopIteration:
            self.report({"ERROR"}, "Logic editor must be open during run")
        return {"FINISHED"}

class StopOperator(bpy.types.Operator):
    bl_idname = "wm.stop"
    bl_label = "Stop"
    bl_description = "Stop all"

    def execute(self, context):
        bpy.types.WindowManager.run = False
        bpy.context.scene.frame_end = 250
        bpy.ops.screen.animation_cancel(restore_frame = True)
        area = next(area for area in bpy.context.screen.areas if area.type == "VIEW_3D")
        area.spaces[0].overlay.show_overlays = True
        area.spaces[0].show_gizmo = True
        area.spaces[0].show_region_header = True
        area.spaces[0].shading.type = "SOLID"
        return {"FINISHED"}

class GameEngineMenu(bpy.types.Menu):
    bl_idname = "GameEngineMenu"
    bl_label = "Game Engine"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.run", icon = "PLAY")
        layout.operator("wm.stop", icon = "PAUSE")
        layout.separator()
        layout.operator("wm.build_menu", icon = "DISK_DRIVE")

def drawItem(self, context):
    layout = self.layout
    layout.menu(GameEngineMenu.bl_idname)

class GameEnginePanel(bpy.types.Panel):
    bl_idname = "GameEnginePanel"
    bl_label = "Game Engine"
    bl_category = "Game Engine"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text = "Assigned object:")
        try:
            layout.label(text = bpy.context.active_node["object"].name)
        except:
            pass
        layout.operator("wm.assign_script", icon = "LINKED")
        layout.separator()
        row = layout.row()
        row.operator("wm.run", icon = "PLAY")
        row.operator("wm.stop", icon = "PAUSE")
        layout.operator("wm.variable", icon = "NETWORK_DRIVE")
        layout.separator()
        layout.operator("wm.build_menu", icon = "DISK_DRIVE")

class AssignScriptOperator(bpy.types.Operator):
    bl_idname = "wm.assign_script"
    bl_label = "Assign Script"
    bl_description = "Assign selected output node to selected object"

    def execute(self, context):
        global id
        bpy.context.active_node["object"] = bpy.context.active_object
        return {"FINISHED"}

class MenuOperator(bpy.types.Operator):
    bl_idname = "wm.menu"
    bl_label = "Game Engine Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu(name = "GameEngineMenu")
        return {"FINISHED"}

class ReportOperator(bpy.types.Operator):
    bl_idname = "wm.report"
    bl_label = "Error Operator"
    rep = None

    def execute(self, context):
        self.report({"ERROR"}, self.rep)
        return {"FINISHED"}

class VariableOperator(bpy.types.Operator):
    bl_idname = "wm.variable"
    bl_label = "Create Variable"
    variable = bpy.props.StringProperty(name = "Variable")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        bpy.types.Object.variables.update({self.variable: 0.0})
        return {"FINISHED"}

class EventOperator(bpy.types.Operator):
    bl_idname = "wm.event"
    bl_label = "Event Operator"

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, e):
        bpy.types.WindowManager.event = e
        bpy.types.WindowManager.mouse = (e.mouse_x, e.mouse_y)
        return self.execute(context)

class BuildMenuOperator(bpy.types.Operator):
    bl_idname = "wm.build_menu"
    bl_label = "Build"
    bl_description = "Build game to current platform"

    def execute(self, context):
        bpy.ops.wm.build("INVOKE_DEFAULT")
        return {"FINISHED"}

class BuildOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "wm.build"
    bl_label = "Build"
    filename_ext = ""
    platform = bpy.props.EnumProperty(
        name = "Platform",
        items = (("1", "Windows", "Build for Windows"), ("2", "Mac OSX", "Build for Mac OSX"), ("3", "Linux", "Build for Linux"))
    )

    def build(self, context):
        if int(self.platform) == 1:
            file = open(self.filepath + ".bat", "w", encoding = "utf-8")
            file.write("ECHO ON\nREM Execute build file\nSET PATH=%PATH%;C:\\Python38\n\"" + bpy.app.binary_path + "\" " + bpy.data.filepath + " --python \"" + bpy.utils.user_resource("SCRIPTS", "addons") + "\\neuro-bge-master\\build.py\"")
            file.close()
        elif int(self.platform) == 2:
            import os
            file = open(self.filepath + ".command", "w", encoding = "utf-8")
            file.write("#!/bin/bash\n\"" + bpy.app.binary_path + "\" " + bpy.data.filepath + " --python \"" + bpy.utils.user_resource("SCRIPTS", "addons") + "\\neuro-bge-master\\build.py\"")
            file.close()
            os.system("chmod +x " + self.filepath + ".command")
        elif int(self.platform) == 3:
            import os
            file = open(self.filepath + ".sh", "w", encoding = "utf-8")
            file.write("#!/bin/bash\n\"" + bpy.app.binary_path + "\" " + bpy.data.filepath + " --python \"" + bpy.utils.user_resource("SCRIPTS", "addons") + "\\neuro-bge-master\\build.py\"")
            file.close()
            os.system("chmod +x " + self.filepath + ".sh")
        elif int(self.platform) == 4:
            pass
        elif int(self.platform) == 5:
            pass
        return {"FINISHED"}

    def execute(self, context):
        return self.build(context)

class AddTriggerOperator(bpy.types.Operator, bpy_extras.object_utils.AddObjectHelper):
    bl_idname = "mesh.trigger"
    bl_label = "Add Trigger Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        verts = [
            mathutils.Vector((-1, 1, -1)),
            mathutils.Vector((1, 1, -1)),
            mathutils.Vector((1, -1, -1)),
            mathutils.Vector((-1, -1, -1)),
            mathutils.Vector((-1, 1, 1)),
            mathutils.Vector((1, 1, 1)),
            mathutils.Vector((1, -1, 1)),
            mathutils.Vector((-1, -1, 1)),
        ]
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7],
        ]
        faces = []
        mesh = bpy.data.meshes.new(name = "Trigger")
        mesh.from_pydata(verts, edges, faces)
        bpy_extras.object_utils.object_data_add(context, mesh, operator = self)
        return {"FINISHED"}

def addTrigger(self, context):
    self.layout.operator("mesh.trigger", text = "Trigger", icon = "MOD_WIREFRAME")
    context.active_object["trigger"] = True

def collision(object1, object2):
    box1 = [object1.matrix_world @ mathutils.Vector(corner) for corner in object1.bound_box]
    box2 = [object2.matrix_world @ mathutils.Vector(corner) for corner in object2.bound_box]
    x_max = max([e[0] for e in box1])
    x_min = min([e[0] for e in box1])
    y_max = max([e[1] for e in box1])
    y_min = min([e[1] for e in box1])
    z_max = max([e[2] for e in box1])
    z_min = min([e[2] for e in box1])
    x_max2 = max([e[0] for e in box2])
    x_min2 = min([e[0] for e in box2])
    y_max2 = max([e[1] for e in box2])
    y_min2 = min([e[1] for e in box2])
    z_max2 = max([e[2] for e in box2])
    z_min2 = min([e[2] for e in box2])
    collision = ((x_max >= x_min2 and x_max <= x_max2) or (x_min <= x_max2 and x_min >= x_min2)) and ((y_max >= y_min2 and y_max <= y_max2) or (y_min <= y_max2 and y_min >= y_min2)) and ((z_max >= z_min2 and z_max <= z_max2) or (z_min <= z_max2 and z_min >= z_min2))
    return collision

def report(report):
    ReportOperator.rep = report
    bpy.ops.wm.report()

def runScript(self, script = "Script"):
    for output in self.outputs:
        if output.name == script:
            for node in output.links:
                node.to_node.runScript()
    if "object" in self:
        return self["object"]
    else:
        for base in self.__class__.__bases__:
            if base.__name__ == "ActionNode" or base.__name__ == "InputNode":
                output = self
                while output.bl_idname != "Output":
                    node = output
                    for outputs in node.outputs:
                        for links in outputs.links:
                            output = links.to_node
                try:
                    return output["object"]
                except KeyError:
                    report("Output does not contain object assignment")

nodeCategories = [
    NodeCategory("EVENTINPUTNODES", "Event", items = [
        nodeitems_utils.NodeItem("OnRunEvent", label = "On Run"),
        nodeitems_utils.NodeItem("OnKeyEvent", label = "On Key", settings = {"Key": repr(1.0)}),
        nodeitems_utils.NodeItem("OnClickEvent", label = "On Click"),
        nodeitems_utils.NodeItem("OnInteractionEvent", label = "On Interaction"),
    ]),
    NodeCategory("INPUTNODES", "Input", items = [
        nodeitems_utils.NodeItem("ObjectPositionInput", label = "Object Position"),
        nodeitems_utils.NodeItem("ObjectRotationInput", label = "Object Rotation"),
        nodeitems_utils.NodeItem("ObjectScaleInput", label = "Object Scale"),
        nodeitems_utils.NodeItem("MouseInput", label = "Mouse"),
        nodeitems_utils.NodeItem("ObjectiveInput", label = "Objective"),
        nodeitems_utils.NodeItem("InteractionInput", label = "Interaction"),
        nodeitems_utils.NodeItem("GravityInput", label = "Gravity"),
        nodeitems_utils.NodeItem("CustomPropertyInput", label = "Custom Property"),
    ]),
    NodeCategory("OUTPUTNODES", "Output", items = [
        nodeitems_utils.NodeItem("Output", label = "Output"),
    ]),
    NodeCategory("ACTIONNODES", "Action", items = [
        nodeitems_utils.NodeItem("MoveAction", label = "Move"),
        nodeitems_utils.NodeItem("RotateAction", label = "Rotate"),
        nodeitems_utils.NodeItem("ScaleAction", label = "Scale"),
        nodeitems_utils.NodeItem("SetTransformAction", label = "Set Transform"),
        nodeitems_utils.NodeItem("ScriptAction", label = "Script"),
        nodeitems_utils.NodeItem("ParentAction", label = "Parent"),
        nodeitems_utils.NodeItem("RemoveParentAction", label = "Remove Parent"),
        nodeitems_utils.NodeItem("VisibilityAction", label = "Visibility"),
        nodeitems_utils.NodeItem("SetGravityAction", label = "Set Gravity"),
        nodeitems_utils.NodeItem("SetCustomPropertyAction", label = "Set Custom Property"),
        nodeitems_utils.NodeItem("PointAtAction", label = "Point At"),
    ]),
    NodeCategory("LOOPNODES", "Logic", items = [
        nodeitems_utils.NodeItem("RepeatLoop", label = "Repeat"),
        nodeitems_utils.NodeItem("RepeatUntilLoop", label = "Repeat Until"),
        nodeitems_utils.NodeItem("WhileLoop", label = "While"),
        nodeitems_utils.NodeItem("IfLogic", label = "If"),
        nodeitems_utils.NodeItem("VariableInput", label = "Variable", settings = {"Variable": repr(1.0)}),
        nodeitems_utils.NodeItem("SetVariableAction", label = "Set Variable", settings = {"Variable": repr(1.0)}),
        nodeitems_utils.NodeItem("DelayAction", label = "Delay"),
        nodeitems_utils.NodeItem("MergeScriptAction", label = "Merge Script"),
        nodeitems_utils.NodeItem("ModeratorLogic", label = "Moderator"),
    ]),
    NodeCategory("CONVERTERNODES", "Converter", items = [
        nodeitems_utils.NodeItem("MathInput", label = "Math", settings = {"Operators": repr(1.0)}),
        nodeitems_utils.NodeItem("VectorMathInput", label = "Vector Math", settings = {"Operators": repr(1.0)}),
        nodeitems_utils.NodeItem("VectorTransformInput", label = "Vector Transform", settings = {"Operators": repr(1.0)}),
        nodeitems_utils.NodeItem("ComparisonLogic", label = "Comparison"),
        nodeitems_utils.NodeItem("SeperateVectorInput", label = "Seperate Vector"),
        nodeitems_utils.NodeItem("CombineVectorInput", label = "Combine Vector"),
        nodeitems_utils.NodeItem("GateLogic", label = "Gate"),
        nodeitems_utils.NodeItem("DegreesToRadiansInput", label = "Degrees To Radians"),
        nodeitems_utils.NodeItem("RadiansToDegreesInput", label = "Radians To Degrees"),
        nodeitems_utils.NodeItem("DistanceInput", label = "Distance"),
    ]),
    NodeCategory("CONTROLLERNODES", "Controller", items = [
        nodeitems_utils.NodeItem("PlayerController", label = "Player Controller"),
        nodeitems_utils.NodeItem("UIController", label = "UI Controller"),
        nodeitems_utils.NodeItem("SceneController", label = "Scene Controller"),
         nodeitems_utils.NodeItem("AudioController", label = "Audio Controller"),
    ]),
]
classes = (LogicEditor, OnKeyEvent, Output, GameEngineMenu, RunOperator, OnRunEvent, MoveAction, GameEnginePanel, AssignScriptOperator, MenuOperator, StopOperator, ObjectPositionInput, ReportOperator, RepeatLoop, MathInput, VectorMathInput, VectorTransformInput, IfLogic, ComparisonLogic, SeperateVectorInput, CombineVectorInput, GateLogic, RotateAction, ScaleAction, VariableOperator, VariableInput, ObjectRotationInput, ObjectScaleInput, SetVariableAction, EventOperator, SetTransformAction, MouseInput, DegreesToRadiansInput, RadiansToDegreesInput, OnClickEvent, DistanceInput, ObjectiveInput, InteractionInput, ScriptAction, RepeatUntilLoop, WhileLoop, ParentAction, RemoveParentAction, DelayAction, MergeScriptAction, ModeratorLogic, VisibilityAction, SetGravityAction, GravityInput, OnInteractionEvent, PlayerController, BuildMenuOperator, BuildOperator, UIController, SceneController, SetCustomPropertyAction, CustomPropertyInput, AudioController, PointAtAction, AddTriggerOperator)
addonKeymaps = []

@persistent
def update(scene):
    if bpy.types.WindowManager.run:
        bpy.ops.object.select_all(action = "DESELECT")
        try:
            for nodeTree in bpy.data.node_groups:
                for node in nodeTree.nodes:
                    if hasattr(node, "continuousUpdate"):
                        node.updateNode()
                    if hasattr(node, "nodeType"):
                        if len(node.inputs) > 0:
                            if node.nodeType == "InputNode" and node.inputs[0].default_value:
                                for input in node.inputs:
                                    if len(input.links) == 0:
                                        node.callConnected()
                                        for i in range(len(node.outputs)):
                                            for j in range(len(node.outputs[i].links)):
                                                node.outputs[i].links[j].to_socket.default_value = node.outputs[i].default_value
                    if node.bl_idname == "VariableInput":
                        node.callConnected()
                        for i in range(len(node.outputs)):
                            for j in range(len(node.outputs[i].links)):
                                node.outputs[i].links[j].to_socket.default_value = node.outputs[i].default_value
        except StopIteration:
            pass

@persistent
def retrieveEvents(scene):
    bpy.ops.wm.event("INVOKE_DEFAULT")

@persistent
def storeData(scene):
    bpy.context.scene["variables"] = str(bpy.types.Object.variables)

def register():
    bpy.types.Object.variables = {}
    for cls in classes:
        bpy.utils.register_class(cls)
    nodeitems_utils.register_node_categories("LOGIC_NODES", nodeCategories)
    bpy.app.timers.register(update)
    bpy.types.VIEW3D_HT_header.append(drawItem)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name = "Object Mode", space_type = "EMPTY")
    kmi = km.keymap_items.new("wm.menu", "E", "PRESS")
    addonKeymaps.append(km)
    bpy.app.handlers.frame_change_pre.append(update)
    bpy.app.handlers.frame_change_pre.append(retrieveEvents)
    bpy.app.handlers.save_pre.append(storeData)
    bpy.types.VIEW3D_MT_add.append(addTrigger)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    nodeitems_utils.unregister_node_categories("LOGIC_NODES")
    bpy.app.timers.unregister(update)
    bpy.types.VIEW3D_HT_header.remove(drawItem)
    wm = bpy.context.window_manager
    for km in addonKeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addonKeymaps.clear()
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.save_pre.clear()
    bpy.types.VIEW3D_MT_add.remove(addTrigger)

if __name__ == "__main__":
    try:
        nodeitems_utils.unregister_node_categories("LOGIC_NODES")
    finally:
        import ast
        bpy.types.Object.variables = ast.literal_eval(bpy.context.scene["variables"])
        register()
