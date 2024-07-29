import pandas as pd

def main():
    """
    Load a CSV file, extract unique state names, and save them to a new CSV file.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv('emissions.csv')

    # Extract unique state names
    unique_states = df['state-name'].unique()

    # Convert to DataFrame
    unique_states_df = pd.DataFrame(unique_states, columns=['state-name'])

    # Save to a new CSV file
    unique_states_df.to_csv('state_names.csv', index=False)

    print("Unique state names have been saved to state_names.csv")

if __name__ == "__main__":
    main()
