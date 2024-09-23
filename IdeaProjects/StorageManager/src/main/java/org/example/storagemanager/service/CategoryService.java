package org.example.storagemanager.service;


import lombok.AllArgsConstructor;
import org.example.storagemanager.dto.CategoryDTO;
import org.example.storagemanager.entity.Category;
import org.example.storagemanager.repository.CategoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class CategoryService {
    private final CategoryRepository categoryRepository;

       public List<Category> readAllCategory(){
           return categoryRepository.findAll();
       }

       public Category readById(Long id){
        return categoryRepository.findById(id).orElseThrow(()->
                new RuntimeException("Category not found - " + id));
    }

    public Category createCategory(CategoryDTO categoryDTO) {
        Category category = Category.builder()
                        .name(categoryDTO.getName())
                        .build();
        return categoryRepository.save(category);
       }
}
