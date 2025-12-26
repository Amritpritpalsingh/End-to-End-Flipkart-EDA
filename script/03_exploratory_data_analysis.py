import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# Load data
df = pd.read_csv("data/clean/cleaned_flipkart.csv")


# Univariate Analysis


plt.figure(figsize=(8,6))
sns.countplot(y="Company", data=df)
plt.title("Company Distribution")
plt.savefig("plots/company_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.countplot(y="Display_Type", data=df)
plt.title("Display Type Distribution")
plt.savefig("plots/display_type_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.countplot(y="Display_Size", data=df)
plt.title("Display Size Distribution")
plt.savefig("plots/display_size_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.countplot(x="Ram", data=df)
plt.title("RAM Distribution")
plt.savefig("plots/ram_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.countplot(y="Rom", data=df)
plt.title("ROM Distribution")
plt.savefig("plots/rom_distribution.png", dpi=300, bbox_inches="tight")
plt.close()


# Bivariate Analysis


plt.figure(figsize=(8,6))
sns.barplot(x="Ram", y="Original_Price", data=df)
plt.title("Original Price by RAM")
plt.savefig("plots/original_price_by_ram.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.barplot(x="Rom", y="Original_Price", data=df)
plt.title("Original Price by ROM")
plt.savefig("plots/original_price_by_rom.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.barplot(x="Original_Price", y="Company", data=df)
plt.title("Original Price by Company")
plt.savefig("plots/original_price_by_company.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8,6))
sns.barplot(x="Discounted_Price", y="Company", data=df)
plt.title("Discounted Price by Company")
plt.savefig("plots/discounted_price_by_company.png", dpi=300, bbox_inches="tight")
plt.close()


# RAM & ROM vs Price (Melted)


df_melted = df.melt(
    id_vars="Ram",
    value_vars=["Original_Price", "Discounted_Price"],
    var_name="Price_Type",
    value_name="Price"
)
plt.figure(figsize=(8,6))
sns.barplot(x="Ram", y="Price", hue="Price_Type", data=df_melted)
plt.title("Average Price by RAM")
plt.savefig("plots/average_price_by_ram.png", dpi=300, bbox_inches="tight")
plt.close()

df_melted = df.melt(
    id_vars="Rom",
    value_vars=["Original_Price", "Discounted_Price"],
    var_name="Price_Type",
    value_name="Price"
)
plt.figure(figsize=(8,6))
sns.barplot(y="Rom", x="Price", hue="Price_Type", data=df_melted, orient="h")
plt.title("Average Price by ROM")
plt.savefig("plots/average_price_by_rom.png", dpi=300, bbox_inches="tight")
plt.close()


# Correlation Heatmap


plt.figure(figsize=(6,4))
sns.heatmap(
    df[["Ram", "Rom", "Original_Price", "Discounted_Price"]].corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.savefig("plots/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
