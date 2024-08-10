import os
import hashlib
from send2trash import send2trash

def calculate_hash(file_path, chunk_size=8192):
    """Calculates the hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    """Finds duplicate files in a directory and its subdirectories."""
    hashes = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)
            
            if file_hash in hashes:
                duplicates.append((file_path, hashes[file_hash]))
            else:
                hashes[file_hash] = file_path

    return duplicates

def save_duplicates_to_file_and_move_to_trash(duplicates, output_file):
    """Saves the paths of duplicate photos to a text file and moves them to the trash."""
    with open(output_file, 'w') as f:
        if duplicates:
            f.write("Duplicate photos found:\n")
            for dup in duplicates:
                f.write(f"Duplicate: {dup[0]}\n")
                f.write(f"Original: {dup[1]}\n\n")
                try:
                    send2trash(dup[0])
                except Exception as e:
                    f.write(f"Error to move {dup[0]} to trash: {e}\n")
        else:
            f.write("No duplicate photos found.\n")

def main():
    directory = "D:\\"  # Substitua pelo caminho da sua pasta
    output_file = "duplicated_photos.txt"  # Nome do arquivo de saída

    duplicates = find_duplicates(directory)
    save_duplicates_to_file_and_move_to_trash(duplicates, output_file)

    print(f"Results saved in {output_file} and duplicate photos moved to trash.")

if __name__ == "__main__":
    main()
