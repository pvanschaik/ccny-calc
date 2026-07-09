# CCNY Calculus 1 Final Project: Solar Cell Placement Effectiveness

## Project Goal
Model the effectiveness of solar panel placement on **Montefiore Square** (CCNY campus redesign project) using calculus and optimization techniques.

## Key Calculus Topics Covered

- **Integration**: Daily energy production via definite integrals
- **Optimization**: Lagrange multipliers and gradient descent for finding optimal panel orientation
- **Multivariable Calculus**: Energy as a function of tilt angle, azimuth, temperature, and time
- **Differential Equations** (optional): Modeling dynamic shadow movement
- **Trigonometry & Spherical Geometry**: Solar position and angle calculations

## Repository Structure

```
ccny-calc/
├── solar_cell_model.py       # Core mathematical model
├── PROJECT_PROPOSAL.md       # Detailed project scope and math
├── analysis.py               # (To be created) Data analysis and visualization
├── REPORT.md                 # (To be created) Final mathematical report
└── README.md                 # This file
```

## Quick Start

### Requirements
```bash
pip install numpy scipy matplotlib
```

### Run the Model
```bash
python solar_cell_model.py
```

Expected output:
```
Solar Cell Placement Effectiveness Model
==================================================

Optimizing for June 21 (Summer Solstice)...
Optimal Tilt: [angle]°
Optimal Azimuth: [direction]° (0°=North, 180°=South)
Expected Daily Energy: [energy] kWh
```

## Model Overview

The model calculates solar panel energy production using:

1. **Solar Position** - Ephemeris calculations for sun elevation and azimuth
2. **Panel Orientation** - Tilt and azimuth angles affecting incident angle
3. **Energy Irradiance** - Direct normal irradiance with atmospheric effects
4. **Panel Efficiency** - Angle and temperature dependent efficiency

### Key Equations

#### Solar Elevation Angle
$$\sin(\alpha_s) = \sin(\phi) \sin(\delta) + \cos(\phi) \cos(\delta) \cos(H)$$

#### Angle of Incidence
$$\cos(\theta) = \vec{n} \cdot \vec{s}$$

#### Daily Energy Production (Integration)
$$E_{daily} = \int_6^{18} I_{dni}(t) \cdot A \cdot \eta(t) \, dt$$

#### Optimization
$$\max_{\alpha, \beta} E(\alpha, \beta) \text{ where } \alpha \in [0°, 90°], \beta \in [0°, 360°]$$

## Montefiore Square Context

**Location**: CCNY Campus, Harlem, NYC
- **Latitude**: 40.8°N
- **Typical dimensions**: ~100m × 150m (estimated)
- **Goal**: Assess solar potential for campus sustainability

## Project Stages

| Stage | Status | Deliverable |
|-------|--------|-------------|
| 1. Model Development | ✅ Complete | `solar_cell_model.py` |
| 2. Analysis & Visualization | 🔄 In Progress | `analysis.py` |
| 3. Mathematical Report | ⏳ Planned | `REPORT.md` |
| 4. Final Presentation | ⏳ Planned | Slides + Demo |

## Contact & Collaboration

This is a collaborative project for CCNY Calculus 1. For questions about:
- **Mathematics**: See `PROJECT_PROPOSAL.md`
- **Code**: Check comments in `solar_cell_model.py`
- **Results**: Coming in `analysis.py`

---

*Project Repository: https://github.com/pvanschaik/ccny-calc*
