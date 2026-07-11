from datasets import load_dataset

# Download Banking77 dataset
dataset = load_dataset(
    "PolyAI/banking77",
    trust_remote_code=True
)

print(dataset)

# Save as CSV
dataset["train"].to_csv("banking77_train.csv", index=False)
dataset["test"].to_csv("banking77_test.csv", index=False)

print("✅ Banking77 dataset downloaded successfully!")