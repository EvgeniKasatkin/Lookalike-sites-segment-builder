A simple attempt to consistently build a segment of the most popular sites similar to the central one. It is based on the idea of ​​the k-means clustering algorithm.
1. The central site is defined, which is interpreted as the center of the k-means algorithm cluster.
2. Then, via RapidAPI, a request is made to ChatGPT to form the top 10 sites similar to the central one. The rank in the sequence of 10 sites is determined by an analogue of the distance of the k-means algorithm.
3. Then, a request is made to ChatGPT for the next 10 received sites and the rank of this sequence is determined similarly.
4. After the iterative responses received, the sum of the products of the query order numbers and the received ranks is analyzed.
5. The resulting list of sites is sorted from smallest to largest, thereby obtaining a sorted list of sites similar to the central one.
