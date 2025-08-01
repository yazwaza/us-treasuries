#runs the view and the controller
from controller.nelsonSiegelController import NelsonSiegelController
from controller.spreadController import SpreadController
from controller.cubicSplineController import CubicSplineController
from controller.butterflySpreadController import ButterflyController

def main():
    # controller = NelsonSiegelController()
    # controller.run_with_warm_start()

    # spread_controller = SpreadController()
    # spread_controller.run()

    # cubic_spline_controller = CubicSplineController()
    # cubic_spline_controller.run()

    butterfly_controller = ButterflyController()
    butterfly_controller.run()

if __name__ == "__main__":
    main()
    # This will run the main function when the script is executed