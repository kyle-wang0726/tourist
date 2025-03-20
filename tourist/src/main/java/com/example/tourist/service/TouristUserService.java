package com.example.tourist.service;

import com.example.tourist.entity.TouristUser;
import com.example.tourist.repository.TouristUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class TouristUserService {
    @Autowired
    private TouristUserRepository userRepository;

    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    /**
     * 注册用户（加密密码后存入数据库）
     */
    public TouristUser registerUser(TouristUser user) {
        user.setPassword(passwordEncoder.encode(user.getPassword())); // 加密密码
        return userRepository.save(user);
    }

    /**
     * 根据用户名查找用户
     */
    public Optional<TouristUser> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    /**
     * 根据邮箱查找用户
     */
    public Optional<TouristUser> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    /**
     * 保存用户
     */
    public void saveUser(TouristUser user) {
        userRepository.save(user);
    }

    /**
     * 校验用户登录（使用 BCrypt 进行密码匹配）
     */
    public boolean validateUser(String username, String password) {
        Optional<TouristUser> userOpt = userRepository.findByUsername(username);
        if (userOpt.isPresent()) {
            return passwordEncoder.matches(password, userOpt.get().getPassword()); // 使用 BCrypt 进行匹配
        }
        return false;
    }
}
