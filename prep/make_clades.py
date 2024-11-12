# -*- coding: utf-8 -*-
"""
Created on Thu May 25 2023

@author: Jenn Knapp
email: jknapp@uwaterloo.ca
"""
"""
Purpose: Retrieve clade-definining mutations from any nextstrain phylogenetic tree
    and create clade definition .json files 
Reguires:
phylogenetic_tree.json (downloaded from nextstrain.org)

flu_seasonal_h3n2_ha_12y.json
clades/

"""
import json
import os

def process_phylogenetic_tree(tree):
    """
    Process the phylogenetic tree and generate JSON files for each clade.
    """
    print("Processing phylogenetic tree...")
    clades = set()
    traverse_tree(tree["tree"], clades)  # Traverse the tree to collect unique clade names
    for clade_name in clades:
        clade_mutations = extract_all_mutations(tree["tree"], clade_name)  # Extract mutations for the clade
        write_json_file(clade_name, clade_mutations)  # Write mutations to a JSON file
        print(f"Processed clade: {clade_name}")
    print("Processing completed.")

def traverse_tree(clade, clades):
    """
    Traverse the phylogenetic tree to collect unique clade names.
    """
    if "node_attrs" in clade and "clade_membership" in clade["node_attrs"]:
        clades.add(clade["node_attrs"]["clade_membership"]["value"])  # Add clade name to the set

    if "children" in clade:
        for child in clade["children"]:
            traverse_tree(child, clades)  # Recursively traverse child nodes

def extract_unique_clades(clade):
    """
    Extract unique clade names from a given clade and its descendants.
    """
    clades = set()
    if "node_attrs" in clade and "clade_membership" in clade["node_attrs"]:
        clades.add(clade["node_attrs"]["clade_membership"]["value"])  # Add clade name to the set

    if "children" in clade:
        for child in clade["children"]:
            child_clades = extract_unique_clades(child)  # Recursively extract clades from child nodes
            clades.update(child_clades)  # Add child clades to the set

    return clades

def process_clade(clade):
    """
    Process a specific clade by extracting its mutations and processing its children.
    """
    clade_name = clade["node_attrs"]["clade_membership"]["value"]
    clade_mutations = extract_all_mutations(clade, clade_name)  # Extract mutations for the clade

    # Print debugging information
    print(f"Processing clade: {clade_name}")
    print(f"Clade mutations: {clade_mutations}")

    for child in clade.get("children", []):
        process_clade(child)  # Recursively process child nodes

    write_json_file(clade_name, clade_mutations)  # Write mutations to a JSON file

def extract_all_mutations(clade, target_clade=None):
    """
    Extract all mutations from a specific clade and its parent nodes.
    If a target clade is provided, only mutations from that clade are extracted.
    """
    mutations = set()
    if "branch_attrs" in clade and "mutations" in clade["branch_attrs"]:
        branch_mutations = clade["branch_attrs"]["mutations"]
        if "nuc" in branch_mutations:
            mutations.update(branch_mutations["nuc"])

    if target_clade and "node_attrs" in clade and "clade_membership" in clade["node_attrs"]:
        clade_membership = clade["node_attrs"]["clade_membership"]["value"]
        if clade_membership == target_clade:
            return list(mutations)  # Return mutations if target clade is found

    if "children" in clade:
        for child in clade["children"]:
            child_mutations = extract_all_mutations(child, target_clade)  # Extract mutations from child nodes
            mutations.update(child_mutations)  # Add child mutations to the set

    return list(mutations)

def write_json_file(clade_name, clade_mutations):
    """
    Write clade mutations to a JSON file.
    """
    data = {
        "label": clade_name,
        "description": f"{clade_name} defining mutations",
        "sources": [],
        "tags": [clade_name],
        "sites": list(clade_mutations),  # Convert mutations set to a list
        "note": "Unique mutations for sublineage",
        "rules": {
            "default": {
                "min_alt": "",
                "max_ref": ""
            },
            "Probable": {
                "min_alt": "",
                "max_ref": ""
            }
        }
    }

    output_dir = "clades"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{clade_name}.json")
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Generated JSON file: {filename}")
    except IOError:
        print(f"Error writing JSON file: {filename}")

# Load the input phylogenetic tree from a JSON file
with open("flu_seasonal_h3n2_ha_12y.json", "r") as json_file:
    nextstrain_data = json.load(json_file)

# Process the phylogenetic tree
process_phylogenetic_tree(nextstrain_data)

