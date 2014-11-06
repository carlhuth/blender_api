# This module sets up a modal operator in Blender to act
# as the command listener for external events

commandRateHz = 10
debug = True

import bpy
from . import network

class BLCommandListener(bpy.types.Operator):
	"""Listens for external commands"""
	bl_label = "Command Listener"
	bl_idname = 'wm.command_listener'

	_timer = None
	bpy.types.Scene.commandListenerActive = bpy.props.BoolProperty( name = "commandListenerActive", default=False)
	bpy.context.scene['commandListenerActive'] = False

	def modal(self, context, event):
		if debug and event.type in {'ESC'}:
			return self.cancel(context)

		if debug and event.type == 'TIMER':
			print('Running Command Listener', round(self._timer.time_duration,3))
			command = network.poll(context)
			...

		# set status
		bpy.context.scene['commandListenerActive'] = True
		return {'PASS_THROUGH'}


	def execute(self, context):
		print('Starting Command Listener')

		success = network.init(context)
		...


		if success:
			wm = context.window_manager
			self._timer = wm.event_timer_add(1/commandRateHz, context.window)
			wm.modal_handler_add(self)
			bpy.context.scene['commandListenerActive'] = True
			return {'RUNNING_MODAL'}
		else:
			print('Error connecting to external interface, stopping')
			return {'CANCELLED'}


	def cancel(self, context):
		print('Stopping Command Listener')
		if self._timer:
			wm = context.window_manager
			wm.event_timer_remove(self._timer)
		else:
			print('no timer')

		network.drop(context)
		...
		bpy.context.scene['commandListenerActive'] = False
		return {'CANCELLED'}


	@classmethod
	def poll(cls, context):
		return not bpy.context.scene['commandListenerActive']
		# return True
		

def register():
	bpy.utils.register_class(BLCommandListener)


def unregister():
	bpy.utils.unregister_class(BLCommandListener)


def refresh():
	try:
		register()
	except Exception as E:
		print('re-registering')
		print(E)
		unregister()
		register()
