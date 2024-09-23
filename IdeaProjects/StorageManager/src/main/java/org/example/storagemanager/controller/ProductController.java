package org.example.storagemanager.controller;


import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.example.storagemanager.dto.ProductDTO;
import org.example.storagemanager.entity.Product;
import org.example.storagemanager.service.ProductService;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

 // Adjust to your frontend URL/port
@RestController
@RequestMapping("/products")
@AllArgsConstructor
@CrossOrigin(origins = "http://localhost:63342/")
public class ProductController {

    private final ProductService productService;

     @PostMapping(consumes = {MediaType.MULTIPART_FORM_DATA_VALUE})
     public ResponseEntity<Product> createProduct(
             @RequestParam("productData") String productData,
             @RequestParam(value = "image", required = false) MultipartFile imageFile) throws IOException {

         // Convert JSON string to ProductDTO
         ObjectMapper objectMapper = new ObjectMapper();
         ProductDTO dto = objectMapper.readValue(productData, ProductDTO.class);

         byte[] imageData = null;
         if (imageFile != null && !imageFile.isEmpty()) {
             imageData = imageFile.getBytes();
         }
         for(byte i : imageData) {
             System.out.println(i);
         }
         // Create and save the Product entity
         Product product = productService.createProduct(dto, imageData);

         return new ResponseEntity<>(product, HttpStatus.OK);
     }


     @GetMapping
    public ResponseEntity<List<Product>> readAll() {
        return mappingResponseListProduct(productService.readAll());
    }

    @GetMapping("/category/{id}")
    public ResponseEntity<List<Product>> readByCategoryId(@PathVariable Long id) {
        return mappingResponseListProduct(productService.readByCategoryId(id));
    }

    @PutMapping
    public ResponseEntity<Product> update(@RequestBody Product product) {
        return mappingResponseProduct(productService.updateProduct(product));
    }

    @DeleteMapping("/{id}")
    public HttpStatus delete(@PathVariable Long id) {
        productService.delete(id);
        return HttpStatus.OK;
    }

    private ResponseEntity<Product> mappingResponseProduct(Product product) {
        return new ResponseEntity<>(product, HttpStatus.OK);
    }

    private ResponseEntity<List<Product>> mappingResponseListProduct(List<Product> products) {
        return new ResponseEntity<>(products, HttpStatus.OK);
    }
}
