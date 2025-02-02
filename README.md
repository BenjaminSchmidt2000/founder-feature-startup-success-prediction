# **Prediction of Startup Success Based on Founders' Features**

This project aims to predict startup success by analyzing various features of startup founders, including job experience, education, connectivity, personality traits, and natural language data. Below is a detailed breakdown of the key features and methods used in this project:

---

## **Features Analyzed**

### **1. Job Experience**
- **Creation of Company Success Scores**
- **Utilization of a Company Prestige Score**
- **VC (Venture Capital) Experience**
- **Consulting Experience**
- **Number of Job Experiences**

### **2. Education**
- **University Degree**
- **Utilization of a Company Prestige Score**
- **Creation of University Prestige Scores**

### **3. Connectivity on LinkedIn**
- **Number of LinkedIn Followers**

### **4. Natural Language Processing**
Analysis of LinkedIn data (comments, posts, reactions, and profile descriptions) to create features using:
- **Unsupervised Clustering Models**
- **Sentiment Analysis Models**
- **Supervised Classification Algorithms** (with University Success as the prediction label)
### **5. Personality Prediction**
- **Publicly Available Tweets**:  
  Use tweets labeled with personality traits to train personality prediction models.
- **LinkedIn Profile Labeling**:  
  - Leverage Crunchbase to connect LinkedIn profiles with `X` profiles (formerly Twitter) shared by founders.
  - Predict personality traits of founders who share their `X` profiles on Crunchbase.
  - Use these predictions to label LinkedIn profiles with personality traits.
- **Personality Features for Startup Success Prediction**:  
  Labeled LinkedIn profiles enable personality prediction for founders, which serves as a feature in startup success prediction.
### **6. Final Model**
The final model is designed to:
- Predict startup success based on the aggregated founder features.
- Extract the **relative importance** of various founder features.
---
### **Key Features of This Repository**
- Data preprocessing and feature engineering scripts.
- Machine learning models for personality prediction and startup success prediction.
- Analysis of feature importance for founder traits contributing to startup success.


![image](https://github.com/user-attachments/assets/e2e6bd7f-ea92-48a1-8bad-afcd20a74d61)
