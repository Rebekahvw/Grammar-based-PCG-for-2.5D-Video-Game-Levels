import numpy as np
import scipy
from PIL import Image
import os
import scipy.special  # Import scipy.special
from sklearn.metrics.pairwise import cosine_similarity

def hamming_distance(image_1,image_2):

    """
    From scipy docs:
    The Hamming distance between 1-D arrays u and v, is simply the proportion of disagreeing components in u and v. 
    If u and v are boolean vectors, the Hamming distance is
    """

    image_1 = np.array(image_1)
    image_2 = np.array(image_2)

    hamming_score = scipy.spatial.distance.hamming(image_1.flatten(),image_2.flatten())

    return hamming_score

def image_to_distribution(image):
    # Convert image to grayscale
    image = image.convert("L")
    
    # Convert the image to a NumPy array
    image_array = np.array(image)
    
    # Normalize pixel values to be between 0 and 1
    image_array = image_array / 255.0
    
    # Flatten the array to a 1D array
    flat_array = image_array.flatten()
    
    # Compute the histogram of pixel intensities
    hist, _ = np.histogram(flat_array, bins=256, range=(0, 1))
    
    # Normalize the histogram to obtain a probability distribution
    distribution = hist / np.sum(hist)
    
    return distribution

def kl_divergence(image1, image2):
    # Convert images to probability distributions
    distribution1 = image_to_distribution(image1)
    distribution2 = image_to_distribution(image2)
    
    # Compute the KL divergence
    kl_div = scipy.stats.entropy(distribution1, distribution2)
    
    return kl_div

practice_folder = os.path.join("..", "version_random")
files = os.listdir(practice_folder)
image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
images = [Image.open(os.path.join(practice_folder, file)) for file in image_files]
num_images = len(images)

hamming_distance_array_random = np.array([])

# Calculate Hamming distance for all pairs of images
for i in range(num_images):
    for j in range(i + 1, num_images):
        distance = hamming_distance(images[i], images[j])
        hamming_distance_array_random = np.append(hamming_distance_array_random,distance)
        print(f"Hamming distance between image {i} and image {j}: {distance}")


ave_hamming_random = np.average(hamming_distance_array_random)

f = open("distance_metrics.txt","a")

print("Average Hamming distance was",ave_hamming_random)
f.write("\nRandom\n")
f.write("Average Hamming distance was: "+str(ave_hamming_random))

np.save("new_random_hamming.npy", hamming_distance_array_random)
#np.save("rogue_hamming.npy", hamming_distance_array_random)

kl_divergence_array_random = np.array([])

# Calculate KL-divergence for all pairs of images
for i in range(num_images):
    for j in range(i + 1, num_images):
        divergence = kl_divergence(images[i], images[j])
        kl_divergence_array_random = np.append(kl_divergence_array_random,divergence)
     #   print(f"KL Divergence between image {i} and image {j}: {divergence}")

ave_kl_random = np.average(kl_divergence_array_random)
f.write("\nAverage KL Divergence was: "+str(ave_kl_random))
print("Average KL Divergence was",ave_kl_random)

np.save("new_random_KL_div.npy", kl_divergence_array_random)
#np.save("rogue_KL_div.npy", kl_divergence_array_random)

cosine_array = np.array([])

# Calculate Cosine similarity for all pairs of images
for i in range(num_images):
    for j in range(i + 1, num_images):
        array1 = np.array(images[i]).flatten()
        array2 = np.array(images[j]).flatten()
        similarity = cosine_similarity([array1], [array2])

        print(f"Cosine similarity between image {i} and image {j}: {similarity[0][0]}")

        cosine_array = np.append(cosine_array,similarity)

ave_cosine = np.average(cosine_array)
# mode_cosine = mode(cosine_array)

f.write("\nAverage Cosine Similarity was: "+str(ave_cosine))
f.close()

print("Average Cosine Similarity was",ave_cosine)

np.save("new_random_cosine_sim.npy", cosine_array)
#np.save("rogue_cosine_sim.npy", cosine_array)