package org.example.storagemanager.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;
    private String name;
    private int price;

    @Lob // Large Object annotation to store large data
    private byte[] imageData;

    @ManyToOne
    @JoinColumn(name = "category_id")
    private Category category;
}
