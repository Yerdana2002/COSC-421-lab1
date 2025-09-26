# ===============================
# COSC 421 / 521 - Assignment 1
# Flight Network Analysis
# ===============================
# Student Name: [Your Name]
# Student ID: [Your ID]
# Partner Name: [If applicable]
# Data Collection Date: [Enter the date you collected flight data]
# ===============================

# Install & load igraph
if (!require(igraph)) {
  install.packages("igraph")
  library(igraph)
} else {
  library(igraph)
}

# -------------------------------
# Task 1: Load nodes (airports list)
# -------------------------------
nodes <- read.csv("canadian_airports.csv", header=TRUE)

# -------------------------------
# Task 2: Load edges (connections list)
# -------------------------------
edges <- read.csv("flightnetwork.csv", header=TRUE)

# -------------------------------
# Task 3: Build graph
# -------------------------------
# Fix column names for igraph
colnames(edges) <- c("from", "to")

# Ensure nodes has a 'name' column
if (!"name" %in% colnames(nodes)) {
  if ("code" %in% colnames(nodes)) {
    nodes$name <- nodes$code
  } else {
    nodes$name <- nodes[,1]
  }
}

# Create complete node list from all airports mentioned in edges
all_airport_codes <- unique(c(edges$from, edges$to))
complete_nodes <- data.frame(name = all_airport_codes)

# Merge with original nodes to preserve city information if available
if ("city" %in% colnames(nodes)) {
  complete_nodes <- merge(complete_nodes, nodes, by = "name", all.x = TRUE)
}

# Build the graph
airports <- graph_from_data_frame(d = edges, vertices = complete_nodes, directed = FALSE)

cat("=== QUESTION 0: Data Collection Date ===\n")
cat("Data was collected on: [ENTER YOUR DATA COLLECTION DATE HERE]\n")
cat("Example: September 20, 2025\n\n")

cat("=== QUESTION 1: Nodes and Edges ===\n")
# Code for Question 1
num_nodes <- vcount(airports)
num_edges <- ecount(airports)

cat("Number of nodes:", num_nodes, "\n")
cat("Number of edges:", num_edges, "\n")
cat("Code used: vcount(airports) and ecount(airports)\n\n")

cat("=== QUESTION 2: Network Plot ===\n")
# Code for Question 2
set.seed(123) # For reproducible layout
png("network_plot.png", width = 800, height = 800) # Save plot as image

plot(airports,
     vertex.label = V(airports)$name,
     vertex.size = 8,
     vertex.color = "lightblue",
     vertex.frame.color = "darkblue",
     vertex.label.color = "black",
     vertex.label.cex = 0.7,
     edge.color = "gray",
     edge.width = 1.5,
     layout = layout_with_fr,
     main = "Canadian Airport Network")

dev.off() # Close the plot device

cat("Network plot saved as 'network_plot.png'\n")
cat("Layout used: layout_with_fr (Fruchterman-Reingold)\n")
cat("Code used: plot(airports, vertex.label = V(airports)$name, layout = layout_with_fr, ...)\n\n")

cat("=== QUESTION 3: Degree Analysis ===\n")
# Code for Question 3
deg <- degree(airports)
mean_degree <- mean(deg)

cat("Degree of each airport:\n")
print(deg)

cat("\nMean degree:", round(mean_degree, 2), "\n")

# Most connected airports
sorted_deg <- sort(deg, decreasing = TRUE)
most_connected <- head(sorted_deg, 2)

# Least connected airports (excluding airports with degree 0 if any)
non_zero_deg <- deg[deg > 0]
if (length(non_zero_deg) > 0) {
  least_connected <- head(sort(non_zero_deg), 2)
} else {
  least_connected <- head(sort(deg), 2)
}

cat("Two most connected airports:\n")
for (i in 1:length(most_connected)) {
  cat("  ", names(most_connected)[i], ": ", most_connected[i], "connections\n")
}

cat("Two least connected airports:\n")
for (i in 1:length(least_connected)) {
  cat("  ", names(least_connected)[i], ": ", least_connected[i], "connection(s)\n")
}

cat("Code used: degree(airports), mean(deg), sort(deg, decreasing = TRUE)\n\n")

cat("=== QUESTION 4: Degree Distribution ===\n")
# Code for Question 4
png("degree_histogram.png", width = 600, height = 400)

hist(deg,
     main = "Degree Distribution of Canadian Airports",
     xlab = "Degree",
     ylab = "Frequency",
     col = "lightblue",
     border = "black",
     breaks = seq(0, max(deg)+1, by=1))

dev.off()

cat("Degree histogram saved as 'degree_histogram.png'\n")
cat("Degree sequence vector (first 10 values):", head(deg, 10), "\n")
cat("Code used: hist(deg, main='Degree Distribution', xlab='Degree', ylab='Frequency')\n\n")

cat("=== QUESTION 5: Adjacency Matrix ===\n")
# Code for Question 5
A <- as.matrix(as_adjacency_matrix(airports))
is_symmetric <- isSymmetric(A)

cat("Adjacency matrix dimensions:", dim(A), "\n")
cat("Is the adjacency matrix symmetric?", is_symmetric, "\n")

# Show a small subset of the matrix
if (nrow(A) >= 5) {
  cat("First 5x5 subset of adjacency matrix:\n")
  print(A[1:5, 1:5])
} else {
  cat("Full adjacency matrix:\n")
  print(A)
}

cat("Code used: as.matrix(as_adjacency_matrix(airports)), isSymmetric(A)\n\n")

# -------------------------------
# Additional Network Properties (for completeness)
# -------------------------------
cat("=== Additional Network Analysis ===\n")
cat("Network density:", round(graph.density(airports), 4), "\n")
cat("Is the graph connected?", is.connected(airports), "\n")

# Components analysis
comp <- components(airports)
cat("Number of connected components:", comp$no, "\n")
cat("Size of largest component:", max(comp$csize), "\n")

# Diameter of largest component
if (is.connected(airports)) {
  cat("Network diameter:", diameter(airports), "\n")
} else {
  giant_component <- induced_subgraph(airports, which(comp$membership == which.max(comp$csize)))
  cat("Diameter of largest component:", diameter(giant_component), "\n")
}