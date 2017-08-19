
import logging
import msgpack

from modules.RemoteExec import serialize
from modules.RemoteExec import run_test
from util.WebRequest import WebGetRobust


class PluginInterface_RemoteExec():

	name = 'RemoteExec'
	can_send_partials = True

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.log = logging.getLogger("Main.RemoteExec.Caller")
		self.wg = WebGetRobust()

		self.calls = {
			'callCode'               : self.call_code,
		}

	def call_code(self, code_struct, extra_env=None, *call_args, **call_kwargs):
		self.log.info("RPC Call for %s byte class!" , len(code_struct['source']))
		class_def, call_name = serialize.deserialize_class(code_struct)

		call_env = {
			'wg'     : self.wg,
		}
		if extra_env:
			for key, value in extra_env.items():
				extra_env[key] = value

		instantiated = class_def(**call_env)
		self.log.info("Instantiated instance of %s. Calling member function %s.", class_def, call_name)

		return getattr(instantiated, call_name)(*call_args, **call_kwargs)

	def test(self):
		run_test.run_test(self)