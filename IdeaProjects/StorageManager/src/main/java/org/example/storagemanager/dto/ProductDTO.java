package org.example.storagemanager.dto;

import lombok.Data;
import org.springframework.web.multipart.MultipartFile;


import org.springframework.web.multipart.MultipartFile;
@Data
public class ProductDTO {
  private String name;
  private int price;
  private Long categoryId;
  private MultipartFile image; // This will hold the uploaded image file
}
