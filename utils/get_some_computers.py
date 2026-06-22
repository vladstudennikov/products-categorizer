import pandas as pd
import random
import math
import os
import re

def get_computers(n: int, input_path: str = "amazon_data/computers.csv", output_path: str = None) -> pd.DataFrame:
    if n <= 0:
        raise ValueError("n must be a positive integer.")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")

    df = pd.read_csv(input_path)
    if 'title' not in df.columns:
        raise ValueError("CSV must contain a 'title' column.")

    brands = [
        'dell', 'hp', 'lenovo', 'asus', 'acer', 'apple', 'msi', 'microsoft',
        'samsung', 'razer', 'panasonic', 'gateway', 'lg', 'toshiba', 'sony',
        'gigabyte', 'chuwi', 'beelink', 'minisforum'
    ]

    def extract_brand(title):
        if not isinstance(title, str):
            return 'Other'
        title_lower = title.lower()
        for brand in brands:
            if re.search(rf'\b{brand}\b', title_lower):
                if brand in ['hp', 'msi', 'lg', 'asus']:
                    return brand.upper()
                return brand.capitalize()
        return 'Other'

    df['brand'] = df['title'].apply(extract_brand)
    brand_groups = df[df['brand'] != 'Other'].groupby('brand')
    brand_indices = {brand: list(group.index) for brand, group in brand_groups}
    
    if not brand_indices:
        raise ValueError("No recognizable brands/producers found in the dataset.")

    brand_indices = {b: idxs for b, idxs in brand_indices.items() if len(idxs) > 0}
    num_available_producers = len(brand_indices)

    if n == 1:
        k = 1
    else:
        min_k = max(1, int(math.sqrt(n) * 0.5))
        max_k = min(num_available_producers, max(1, int(math.sqrt(n) * 1.5)))
        min_k = min(min_k, max_k)
        k = random.randint(min_k, max_k)

    k = min(k, n)

    selected_producers = random.sample(list(brand_indices.keys()), k)

    capacities = {producer: len(brand_indices[producer]) for producer in selected_producers}
    total_available = sum(capacities.values())

    if total_available < n:
        raise ValueError(
            f"Requested {n} products, but only {total_available} products are available "
            f"across the selected producers: {list(capacities.keys())}."
        )

    sizes = {producer: 1 for producer in selected_producers}
    remaining = n - k

    active_producers = [p for p in selected_producers if capacities[p] > 1]

    while remaining > 0 and active_producers:
        p = random.choice(active_producers)
        max_add = capacities[p] - sizes[p]
        if max_add <= 0:
            active_producers.remove(p)
            continue
        add = random.randint(1, min(remaining, max_add))
        sizes[p] += add
        remaining -= add
        if sizes[p] >= capacities[p]:
            active_producers.remove(p)

    if remaining > 0:
        for p in selected_producers:
            if remaining <= 0:
                break
            space = capacities[p] - sizes[p]
            if space > 0:
                add = min(remaining, space)
                sizes[p] += add
                remaining -= add

    sampled_indices = []
    for producer, count in sizes.items():
        sampled_indices.extend(random.sample(brand_indices[producer], count))

    sampled_df = df.loc[sampled_indices].copy()
    sampled_df = sampled_df.drop(columns=['brand'])
    if output_path is None:
        output_path = f"amazon_data/computers_{n}.csv"

    sampled_df.to_csv(output_path, index=False)
    print(f"Successfully wrote {n} products from {k} producers to {output_path}.")
    print(f"Selected producers and counts: {sizes}")
    
    return sampled_df

if __name__ == "__main__":
    import sys
    n_val = 10
    if len(sys.argv) > 1:
        try:
            n_val = int(sys.argv[1])
        except ValueError:
            pass
    get_computers(n_val)