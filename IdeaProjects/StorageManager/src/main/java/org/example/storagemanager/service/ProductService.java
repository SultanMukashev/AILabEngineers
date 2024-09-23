package org.example.storagemanager.service;


import lombok.AllArgsConstructor;
import org.example.storagemanager.dto.ProductDTO;
import org.example.storagemanager.entity.Product;
import org.example.storagemanager.repository.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
@AllArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final CategoryService categoryService;

    public Product createProduct(ProductDTO dto, byte[] imageData) {
        // Build the Product entity from DTO and set image data if provided
        Product product = Product.builder()
                .name(dto.getName())
                .price(dto.getPrice())
                .category(categoryService.readById(dto.getCategoryId()))
                .imageData(imageData) // Set image data here
                .build();

        return productRepository.save(product);
    }

    public List<Product> readAll() {
        return productRepository.findAll();
    }

    public List<Product> readByCategoryId(Long id) {
        return productRepository.findByCategoryId(id);
    }

    public Product updateProduct(Product product) {
        return productRepository.save(product);
    }

    public void delete(Long id) {
        productRepository.deleteById(id);
    }
}
