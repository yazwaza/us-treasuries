# US Treasury Yield Curve Analysis

A comprehensive Python toolkit for analyzing US Treasury yield curves using advanced financial modeling techniques including Nelson-Siegel-Svensson curve fitting, cubic spline interpolation, and butterfly spread analysis.

## 🎯 Project Overview

This project provides a complete framework for Treasury yield curve analysis, featuring:

- **Nelson-Siegel-Svensson (NSS) curve fitting** with parameter optimization
- **Cubic spline interpolation** for smooth yield curve construction  
- **Butterfly spread analysis** with mean reversion detection
- **Spread analysis** between different maturities (2Y-5Y, 2Y-10Y)
- **Interactive visualizations** with detailed statistical tables
- **Efficient batch processing** with warm-start optimization

## 📊 Features

### 1. Nelson-Siegel-Svensson Model
- Fits parametric yield curves using the extended Nelson-Siegel model
- Warm-start optimization for improved performance
- Adaptive optimization based on curve fit quality
- R² validation and error analysis by maturity segments

### 2. Cubic Spline Analysis
- Natural, clamped, and not-a-knot boundary conditions
- Smooth curve interpolation between market data points
- Visual comparison with market observations

### 3. Butterfly Spread Analysis
- Traditional butterfly spreads (2Y-5Y-10Y)
- Multilinear regression hedging
- Mean reversion detection with Z-score analysis
- Comparison between market and model-derived spreads

### 4. Spread Analysis
- 2Y-5Y spread analysis with mean reversion testing
- Statistical distribution analysis
- Z-score calculations for trading signals
- Histogram visualizations with confidence bands

## 🗂️ Project Structure

```
us-treasuries/
├── controller/                    # MVC Controllers
│   ├── butterflySpreadController.py
│   ├── cubicSplineController.py
│   ├── nelsonSiegelController.py
│   └── spreadController.py
├── models/                        # Mathematical Models
│   ├── buttefly.py               # Butterfly spread calculations
│   ├── cubicSpline.py            # Cubic spline implementation
│   ├── nelsonSiegelModel.py      # NSS curve fitting
│   └── spreadMeanCalculator.py   # Spread analysis tools
├── view/                         # Visualization Components
│   ├── butterflyView.py
│   ├── cubicSplineView.py
│   ├── nelsonSiegelView.py
│   ├── oneDayView.py
│   └── spreadView.py
├── data/                         # Historical Data
│   ├── 2023.csv
│   ├── 2024.csv
│   └── 2025.csv
├── csvReader.py                  # Data loading utilities
├── main.py                       # Main execution script
├── test.py                       # Unit tests
└── README.md
```

## 📈 Data Format

The project uses US Treasury yield data with the following structure:

| Date | 1 Mo | 2 Mo | 3 Mo | 4 Mo | 6 Mo | 1 Yr | 2 Yr | 3 Yr | 5 Yr | 7 Yr | 10 Yr | 20 Yr | 30 Yr |
|------|------|------|------|------|------|------|------|------|------|------|-------|--------|--------|
| 2025-01-02 | 4.45 | 4.36 | 4.36 | 4.31 | 4.25 | 4.17 | 4.25 | 4.29 | 4.38 | 4.47 | 4.57 | 4.86 | 4.79 |

- **Source**: US Treasury daily yield curve rates
- **Coverage**: 2023-2025 (636 trading days)
- **Maturities**: 1M to 30Y across 13 different tenors

## 🚀 Quick Start

### Prerequisites

```bash
pip install numpy pandas scipy matplotlib scikit-learn
```

### Basic Usage

```python
from main import main

# Run the complete analysis suite
main()
```

### Individual Components

```python
# Nelson-Siegel-Svensson Analysis
from controller.nelsonSiegelController import NelsonSiegelController
nss_controller = NelsonSiegelController()
nss_controller.run_with_warm_start()

# Butterfly Spread Analysis  
from controller.butterflySpreadController import ButterflyController
butterfly_controller = ButterflyController()
butterfly_controller.run()

# Spread Analysis
from controller.spreadController import SpreadController
spread_controller = SpreadController()
spread_controller.run_averages()

# Cubic Spline Analysis
from controller.cubicSplineController import CubicSplineController
cubic_controller = CubicSplineController()
cubic_controller.run()
```

## 🔬 Technical Details

### Nelson-Siegel-Svensson Model

The NSS model fits yield curves using the formula:

```
y(τ) = β₀ + β₁[(1-e^(-τ/λ₀))/(τ/λ₀)] + β₂[((1-e^(-τ/λ₀))/(τ/λ₀)) - e^(-τ/λ₀)] + β₃[((1-e^(-τ/λ₁))/(τ/λ₁)) - e^(-τ/λ₁)]
```

Where:
- `β₀`: Long-term yield level
- `β₁`: Short-term component (slope)
- `β₂`: Medium-term component (curvature)
- `β₃`: Second hump component
- `λ₀, λ₁`: Decay parameters

### Optimization Features

- **Warm-start optimization**: Uses previous day's parameters as starting point
- **Adaptive iteration limits**: 50/200/1000 iterations based on fit quality
- **Bounded optimization**: Prevents parameter explosion
- **Maturity-specific error analysis**: Short/medium/long-term error tracking

### Performance Metrics

- **R² thresholds**: >0.90 (excellent), >0.80 (good), <0.80 (requires intensive optimization)
- **Error analysis**: Separate tracking for 1M-3Y, 5Y-10Y, and 20Y-30Y segments
- **Z-score analysis**: Mean reversion detection for trading signals

## 📊 Sample Outputs

### Nelson-Siegel-Svensson Curve Fitting
- Visual comparison of market data vs. fitted curves
- R² values and error metrics by maturity
- Color-coded tables showing fit quality

### Butterfly Spread Analysis
- Market vs. model butterfly spread comparison
- Z-score distributions for mean reversion analysis
- Regression coefficients for hedging ratios

### Spread Analysis
- Time series plots of yield spreads
- Statistical distribution analysis
- Mean reversion parameters and confidence intervals

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test.py
```

Tests cover:
- Data loading and integrity
- Nelson-Siegel model accuracy
- Butterfly spread calculations
- Error function optimization
- Parameter validation

## 📚 Key Algorithms

### 1. Efficient Warm-Start Optimization
- Reduces computation time by 60-80%
- Maintains fitting accuracy across time series
- Adaptive convergence criteria

### 2. Butterfly Spread Hedging
- Multilinear regression: `Butterfly = β₁(2Y-10Y) + β₂(5Y) + ε`
- Duration-neutral weighting
- Mean reversion detection

### 3. Cubic Spline Interpolation
- Multiple boundary condition options
- Smooth curve construction
- Numerical stability for extreme market conditions

## 🎯 Use Cases

### For Quantitative Analysts
- Yield curve modeling and forecasting
- Risk factor decomposition
- Relative value analysis

### For Traders
- Mean reversion trading signals
- Butterfly spread arbitrage opportunities
- Curve positioning strategies

### For Risk Managers
- Duration and convexity analysis
- Scenario analysis and stress testing
- Model validation and backtesting

## 🔧 Configuration

### Optimization Parameters

```python
# NSS Model bounds
bounds = [
    (1.0, 8.0),    # β₀ (level)
    (-6.0, 6.0),   # β₁ (slope)  
    (-8.0, 8.0),   # β₂ (curvature)
    (-6.0, 6.0),   # β₃ (hump)
    (0.8, 3.5),    # λ₀ (decay1)
    (0.05, 0.4)    # λ₁ (decay2)
]

# Performance thresholds
GOOD_ERROR_THRESHOLD = 0.05
ACCEPTABLE_ERROR_THRESHOLD = 0.15
```

## 📋 Requirements

- Python 3.8+
- NumPy 1.20+
- Pandas 1.3+
- SciPy 1.7+
- Matplotlib 3.4+
- Scikit-learn 1.0+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- US Department of the Treasury for Treasury yield data
- Nelson & Siegel (1987) and Svensson (1994) for the parametric curve model
- SciPy community for optimization algorithms

## 📞 Contact

For questions, suggestions, or collaboration opportunities, please open an issue in the repository.

---

**Built with ❤️ for the quantitative finance community**
