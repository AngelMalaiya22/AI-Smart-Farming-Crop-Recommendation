# Enhanced Crop Recommendation Dataset

## Overview

The **Enhanced Crop Recommendation Dataset** is an improved version of a publicly available crop recommendation dataset obtained from Kaggle (MIT License). The dataset was enhanced through feature engineering to better represent real-world agricultural conditions for machine learning-based crop recommendation systems.

The primary objective of this dataset is to predict the most suitable crop based on soil characteristics, environmental conditions, and geographical information.

---

## Dataset Source

- **Original Dataset:** Crop and Soil Dataset
- **Source:** Kaggle
- **License:** MIT License

---

## Dataset Enhancements

The original dataset was modified to improve its usefulness for crop recommendation research.

### Added Feature

A new feature named **Soil_Type** was introduced using **Rule-Based Feature Engineering**.

The original dataset contained **Soil_Texture** (Clay, Sandy, Silt, Loamy) but did not contain geographical soil types such as Black Soil, Alluvial Soil, Red Soil, Laterite Soil, Desert Soil, Mountain Soil, Marshy Soil, and Alkaline Soil.

The **Soil_Type** feature was manually assigned by considering the combination of:

- Crop Type
- Season
- Region
- Soil Texture

Agricultural domain knowledge was used to determine the most suitable soil type for each agricultural scenario.

This engineered feature enhances the agricultural representation of the dataset and enables experimentation with the impact of soil type on crop recommendation performance.

---

## Features

| Feature | Description |
|----------|-------------|
| N | Nitrogen content in soil |
| P | Phosphorus content in soil |
| K | Potassium content in soil |
| Soil_pH | Soil pH value |
| Soil_Moisture | Moisture content of soil |
| Organic_Carbon | Organic carbon present in soil |
| Temperature | Average temperature (°C) |
| Humidity | Relative humidity (%) |
| Rainfall | Rainfall (mm) |
| Sunlight_Hours | Daily sunlight hours |
| Season | Agricultural season (Kharif, Rabi, Zaid) |
| Soil_Texture | Physical texture of soil (Clay, Sandy, Silt, Loamy) |
| Region | Broad geographical region of India |
| Soil_Type | Engineered feature representing the most suitable soil type |
| Crop_Type | Target variable (Recommended Crop) |

---

## Target Variable

**Crop_Type**

The machine learning models are trained to predict the most suitable crop based on the input soil and environmental parameters.

---

## Feature Engineering

The following feature was engineered:

### Soil_Type

**Technique Used:**
- Rule-Based Feature Engineering

**Methodology:**
- Manual assignment using agricultural domain knowledge
- Considered:
  - Crop Type
  - Season
  - Region
  - Soil Texture

The engineered soil type represents the most suitable soil type for the given agricultural conditions rather than a directly measured field observation.

---

## Intended Use

This dataset is designed for:

- Crop Recommendation Systems
- Machine Learning Research
- Explainable AI (XAI)
- Agricultural Decision Support Systems
- Feature Engineering Studies
- Classification Models

---

## Future Scope

Future versions of the dataset may include:

- State
- District
- GPS Coordinates
- Soil Health Card Parameters
- Weather API Integration
- Real-time Environmental Data

---

## License

The original dataset is licensed under the **MIT License**.

This enhanced version preserves the original license while including additional feature engineering performed for research and educational purposes.
