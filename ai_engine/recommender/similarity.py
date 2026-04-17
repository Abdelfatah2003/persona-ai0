import numpy as np

def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0.0
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

def euclidean_distance(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.linalg.norm(vec1 - vec2)

def manhattan_distance(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.sum(np.abs(vec1 - vec2))

def pearson_correlation(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    if len(vec1) != len(vec2):
        return 0.0
    
    mean1 = np.mean(vec1)
    mean2 = np.mean(vec2)
    
    numerator = np.sum((vec1 - mean1) * (vec2 - mean2))
    denominator = np.sqrt(np.sum((vec1 - mean1) ** 2) * np.sum((vec2 - mean2) ** 2))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator

def cosine_similarity_matrix(matrix):
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = matrix / norms
    return np.dot(normalized, normalized.T)

def find_knn(query_vector, vectors, k=5, metric='cosine'):
    distances = []
    
    for i, vec in enumerate(vectors):
        if metric == 'cosine':
            dist = 1 - cosine_similarity(query_vector, vec)
        elif metric == 'euclidean':
            dist = euclidean_distance(query_vector, vec)
        elif metric == 'manhattan':
            dist = manhattan_distance(query_vector, vec)
        else:
            dist = euclidean_distance(query_vector, vec)
        
        distances.append((i, dist))
    
    distances.sort(key=lambda x: x[1])
    return distances[:k]
