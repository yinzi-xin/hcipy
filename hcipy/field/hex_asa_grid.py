import numpy as np

from .grid import Grid
from .coordinates import UnstructuredCoords

class HexagonalASAGrid(Grid):
	'''A grid representing a two-dimensional hexagonal coordinate system in ASA coordinates
	'''
	_coordinate_system = 'hexasa'

	@property
	def a(self):
		'''The array coordinate (dimension 0)
		'''
		return self.coords[0]

	@property
	def r(self):
		''' The row coordinate (dimension 1)
		'''
		return self.coords[1]

	@property
	def c(self):
		''' The column coordinate (dimension 2)
		'''
		return self.coords[2]

def _cartesian_to_hexasa(self):
	# from .coordinates import UnstructuredCoords

	# x = self.x
	# y = self.y
	# r = np.hypot(x, y)
	# theta = np.arctan2(y, x)
	# return PolarGrid(UnstructuredCoords([r, theta]))

	raise NotImplementedError()

def _hexasa_to_cartesian(self):
	# from .coordinates import UnstructuredCoords
	# from .cartesian_grid import CartesianGrid

	# r = self.r
	# theta = self.theta
	# x = r * np.cos(theta)
	# y = r * np.sin(theta)
	# return CartesianGrid(UnstructuredCoords([x, y]))

	raise NotImplementedError()

Grid._add_coordinate_system('hexasa', HexagonalASAGrid)

Grid._add_coordinate_system_transformation('cartesian', 'hexasa', _cartesian_to_hexasa)
Grid._add_coordinate_system_transformation('hexasa', 'cartesian', _hexasa_to_cartesian)
