package com.example.tourist.repository;

import com.example.tourist.entity.TouristUser;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface TouristUserRepository extends JpaRepository<TouristUser, Long> {
    Optional<TouristUser> findByUsername(String username);
    Optional<TouristUser> findByEmail(String email);
}