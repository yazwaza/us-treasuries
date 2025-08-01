import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

class CubicSplineAnalyzer:

    def __init__(self,df):
        self.df = df
        self.maturities = np.array([
            1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30
        ])

    def calculate_spline(self, y, bc_type='natural'):
        """
        Calculate the cubic spline for the given x and y values.
        
        :param y: The y values (yields).
        :param bc_type: Boundary condition type:
                       'natural' - second derivative is zero at boundaries (default)
                       'clamped' - first derivative is zero at boundaries  
                       'not-a-knot' - third derivative is continuous at second and second-to-last points
        :return: A CubicSpline object representing the spline.
        """

        # Create a cubic spline with specified boundary conditions
        spline = CubicSpline(self.maturities, y, bc_type=bc_type)

        return spline