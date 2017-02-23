import numpy as np

class FourierTransform(object):
	def forward(self, field):
		raise NotImplementedError()
	
	def backward(self, field):
		raise NotImplementedError()
	
	def get_transformation_matrix(self):
		coords_in = self.input_grid.as_('cartesian').coords
		coords_out = self.output_grid.as_('cartesian').coords

		A = np.exp(-1j * np.dot(np.array(coords_out).T, coords_in))
		A *= self.input_grid.weights

		return A

def time_it(function, t_max=5, n_max=100):
	import time
	
	start = time.time()
	times = []
	
	while (time.time() < start + t_max) and (len(times) < n_max):
		t1 = time.time()
		function()
		t2 = time.time()
		times.append(t2 - t1)
	
	return np.median(times)

def make_fourier_transform(input_grid, output_grid=None, q=1, fov=1, planner='estimate'):
	from .fast_fourier_transform import FastFourierTransform, make_fft_grid
	from .matrix_fourier_transform import MatrixFourierTransform

	if output_grid is None:
		# Choose between FFT and MFT
		if not (input_grid.is_regular and input_grid.is_('cartesian')):
			raise ValueError('For non-regular non-cartesian Grids, a Fourier transform is required to have an output_grid.')

		if input_grid.ndim not in [1,2]:
			method = 'fft'
		else:
			output_grid = make_fft_grid(input_grid, q, fov)

			if planner == 'estimate':
				# Estimate analytically from complexities
				N_in = input_grid * q
				N_out = output_grid.shape

				if input_grid.ndim == 1:
					fft = 4 * N_in[0] * np.log2(N_in)
					mft = 4 * input_grid.size * N_out[0]
				else:
					fft = 4 * np.prod(N_in) * np.log2(np.prod(N_in))
					mft = 4 * (np.prod(input_grid.shape) * N_out[1] + np.prod(N_out) * input_grid.shape[0])
				if fft > mft:
					method = 'mft'
				else:
					method = 'fft'
			elif planner == 'measure':
				# Measure directly
				fft = FastFourierTransform(input_grid, q, fov)
				mft = MatrixFourierTransform(input_grid, output_grid)

				a = np.zeros(input_grid.size, dtype='complex')
				fft_time = time_it(lambda: fft.forward(a))
				mft_time = time_it(lambda: mft.forward(a))

				if fft_time > mft_time:
					method = 'mft'
				else:
					method = 'fft'
	else:
		# Choose between MFT and Naive
		if input_grid.is_separable and input_grid.is_('cartesian') and output_grid.is_separable and output_grid.is_('cartesian') and input_grid.ndim in [1,2]:
			method = 'mft'
		else:
			method = 'naive'
	
	# Make the Fourier transform
	if method == 'fft':
		return FastFourierTransform(input_grid, q, fov_factor)
	elif method == 'mft':
		return MatrixFourierTransform(input_grid, output_grid)
	elif method == 'naive':
		return NaiveFourierTransform(input_grid, output_grid)
