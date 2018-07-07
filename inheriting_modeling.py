import tensorflow as tf

def _build_structure_component(bs=object):
	class Representation(bs):
		def __init__(self):
			super(type(object))

	class Inherit(Representation):
		def __init__(self, *args, **kwargs):
			super(type(Representation))

	class ObjectProxy(Inherit):
		def __init__(self, *args, **kwargs):
			self.implementation = kwargs['implementation']
			Inherit.__init__(self, *args, **kwargs)

		def __str__(self):
			return self.implementation

	return ObjectProxy

class BuildPolymorphismConstructorInheritance(_build_structure_component()):
	def __init__(self, *args, **kwargs):
		super(BuildPolymorphismConstructorInheritance)

def build_component(imp=_build_structure_component()):
	class SubTyping(imp):
		def __init__(self, *args, **kwargs):
			super(type(imp))

	class ClassInheritance(SubTyping):
		def __init__(self, *args, **kwargs):
			imp.__init__(self, *args, **kwargs)

	class Polymorphism(ClassInheritance):
		def __init__(self, *args, **kwargs):
			ClassInheritance.__init__(self, *args, **kwargs)

	return Polymorphism

assert type(build_component()) == type(_build_structure_component())