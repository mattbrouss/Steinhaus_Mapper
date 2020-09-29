# Steinhaus Filtration and Stable Paths in the Mapper

### Introduction

This repository presents computations (in Jupyter notebooks) accompanying our manuscript [Steinhaus Filtration and Stable Paths in the Mapper (arXiv:1906.08256)](https://arxiv.org/abs/1906.08256). We outline the computations in separate sections. 

### Requirements

These notebooks require the following packages:

  - os
  - pandas
  - hdbscan
  - matplotlib
  - mnist
  - networkx
  - numpy
  - seaborn
  - sklearn
  - umap
  - kmapper
  - scipy
  - itertools
  - time
  - paths
  - dionysus
  - ripser
  - cechmate

## Comparison of Čech and Cover Filtrations

A *filtration* is a construction on a point cloud that attempts to uncover the topology of the underlying space from which the cloud is sampled by constructing an evolving simplicial complex and noting the changes of the complex's topology as it evolves. This is a method often used in [Topological Data Analysis (TDA)](https://en.wikipedia.org/wiki/Topological_data_analysis). Standard filtration methods such as [Čech  and Vietoris-Rips filtrations](https://en.wikipedia.org/wiki/Vietoris%E2%80%93Rips_complex) build a complex by adding simplices based on nearness of points, relying on an underlying metric space. The cover filtration process creates a filtration of the nerve of a collection of sets by strength of overlap between sets. To situate the two constructions, we compare the Čech filtration for a collection of points with the cover filtration for the collection of sets formed by balls of radius (max distance between points)/2 around the same point cloud.

[ComparisonofCechandCoverFiltrations](ComparisonofCechandCoverFiltrations.ipynb) is the notebook for Section 4 in the manuscript on Equivalence. It constructs both two-dimensional and three-dimensional Čech and cover filtrations from a random point set. To ease computational costs, we subsample the point sets and construct both filtrations, then compare the resulting structures. The goal of this section is to show the similarity of the (approximations of the) Čech and cover filtrations by comparing their persistence diagrams.

The notebook generates diagrams as shown below:

<img src=comparison_of_filtrations.png width=900>

## Stable Paths and Recommendation Systems

The Mapper algorithm is a staple TDA tool that summarizes structure of a point cloud as a simplicial complex (graph, most often) and studies the topology thereof. By considering the points mapped to each node in the Mapper as our base sets, we construct a Mapper from the cover filtration with weights on edges given by the strength of overlap between the two nodes that the edge connects. This allows us to look at the persistence of paths when filtered by strength of overlap. In the use-case for Section 6 on movie recommendations, a path with high persistence would correspond with a *sequence* of movies linked by having large sets of recommenders. This information could be used, for instance, to generate *long range* movie recommendations.

The notebook [PathsonRecSys](PathsonRecSys.ipynb) considers all movies from a standard [MovieLens](https://grouplens.org/datasets/movielens/20m/) movie recommendation database that have sufficiently many recommendations, then subsamples the remaining movies. Then a Mapper graph is constructed by assigning to each movie a set of users who recommended it sufficiently highly. By filtering on strength of connection, the code returns the most stable path from a source movie to a target movie for various lengths of path.

For instance, the notebook returned the following paths from Mulan to Moulin Rouge:

<img src=Mulan_Rouge_Table.png width=600>

## Stable Paths and Fashion MNIST

As an application of Steinhaus filtration to explainable machine learning, we explore outputs from trained learning models on the [FashionMNIST](https://github.com/zalandoresearch/fashion-mnist) data set. The notebook [MapperonFashion](MapperonFashion.ipynb) presents the implementation. We construct a Mapper using the reduced representations of the prediction probabilities from a standard predictive model, and then study the stability of paths in this Mapper. Highly stable paths provide a gradient view of types of clothing (in this case, footwear) which the trained model might consider similar.

We get output such as the following:

<img src=path10.png width=450>


This is a 10-node stable path, with sample sneaker, sandal, and ankle boot representatives from each of the 10 modes (along with some other classes). As we progress along the path, we can see gradual change in the general construction of shoe from a sandal to an ankle boot. Note the higher ankles (or heels) on the sandals and sneakers in the last two rows!
