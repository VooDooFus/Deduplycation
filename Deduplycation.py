import os
import hashlib

def calculate_hash(file_path):
    """Calculate the hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_and_delete_duplicates(directory):
    """Find and delete duplicate files in the specified directory."""
    hash_dict = {}
    duplicates = {}

    # Iterate through each file in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)
            
            # Check if the hash already exists in the dictionary
            if file_hash in hash_dict:
                duplicates[file_path] = hash_dict[file_hash]
            else:
                hash_dict[file_hash] = file_path

    # Delete duplicate files and keep track of what's deleted
    deleted_files = []
    for file_path, original_path in duplicates.items():
        try:
            os.remove(file_path)
            deleted_files.append((file_path, original_path))
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    return deleted_files

def main():
    directory = 'DIRECTORY'  # Change this to your directory
    print(f"Scanning directory: {directory}")
    deleted_files = find_and_delete_duplicates(directory)

    # Print summary of deleted files
    print("\nSummary:")
    if deleted_files:
        print("Deleted files:")
        for file_path, original_path in deleted_files:
            print(f"  - {file_path} (Duplicate of {original_path})")
    else:
        print("No duplicate files found.")

    print("\nDone!")

if __name__ == "__main__":
    main()
