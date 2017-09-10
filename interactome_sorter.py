import csv

def parse_file(file_path):
    good_lines = list()
    saw_one = False

    with open(file_path, "rb") as f:
        for line in f:
            if line[0][0] == "1":
                saw_one = True

            if saw_one:
                processed_line = line.strip().split("|")
                try:
                    length = processed_line[4]
                    length = length.split(",")
                    length = list([length[1].split(" ")[0], length[6]])

                    product = processed_line[2]
                    product = product.split("product=")[1][:-1]

                    processed_line = {"function": product, "gene_id": length[0], "hits": int(length[1])}

                    good_lines.append(processed_line)
                except IndexError:
                    pass

    return good_lines

def hits_filter(parsed_sample, min_hits):
    filtered_sample = list()

    for line in parsed_sample:
        if line["hits"] >= min_hits:
            filtered_sample.append(line)

    return filtered_sample

def find_uniques(sample, background,factor):
    background = hits_filter(background, 1)
    
    unique_proteins = []
    duplicate_proteins = []

    for sample_protein in sample:
        unique = True
        for background_protein in background:
            if sample_protein["gene_id"] == background_protein["gene_id"]:
                if sample_protein["hits"] <= factor  * background_protein["hits"]: 
                    unique = False
                    duplicate_proteins.append({"SAMPLE":sample_protein, "BACKGROUND":background_protein})

        if unique:
            unique_proteins.append(sample_protein)
    
    assert(len(unique_proteins) + len(duplicate_proteins) == len(sample))

    return unique_proteins, duplicate_proteins

def get_hypotheticals(unique_proteins, save_file=None):
    hypotheticals = []
    non_hypotheticals = []

    for protein in unique_proteins:
        if protein["function"].lower() == "hypothetical protein":
            hypotheticals.append(protein)
        else:
            non_hypotheticals.append(protein)

    if save_file is not None:
        with open(save_file, "wb") as f:
            writer = csv.writer(f)
            writer.writerow(["H"])
            writer.writerow([str(key) for key in hypotheticals[0].keys()])
            for line in hypotheticals:
                writer.writerow([str(value) for value in line.values()])
            
            writer.writerow(["NH"])
            writer.writerow([str(key) for key in hypotheticals[0].keys()])
            for line in non_hypotheticals:
                writer.writerow([str(value) for value in line.values()])
  
    return hypotheticals, non_hypotheticals

if __name__ == "__main__":
    sample_file = "./sample.csv"
    background_file = "./background.csv"
    output_file = "./hypotheticals.csv"    

    sample = parse_file(file_path=sample_file)
    background = parse_file(file_path=background_file)

    filtered_sample = hits_filter(parsed_sample=sample, min_hits=3)

    unique_samples, duplicate_samples = find_uniques(filtered_sample, background, 3)
    
    hypotheticals, non_hypotheticals = get_hypotheticals(unique_samples, save_file=output_file)
