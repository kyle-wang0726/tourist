package com.example.tourist.controller;

import com.example.tourist.entity.TouristUser;
import com.example.tourist.service.TouristUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "http://localhost:5175") // 确保允许前端访问
public class TouristAuthController {

    @Autowired
    private TouristUserService userService;

    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    /**
     * 用户注册
     */
    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody TouristUser user) {
        if (userService.findByUsername(user.getUsername()).isPresent()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("用户名已存在");
        }
        try {
            TouristUser newUser = userService.registerUser(user);
            return ResponseEntity.ok("注册成功");
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("注册失败");
        }
    }

    /**
     * 用户登录
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody TouristUser user) {
        boolean isValid = userService.validateUser(user.getUsername(), user.getPassword());
        if (isValid) {
            return ResponseEntity.ok().body("登录成功");
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("用户名或密码错误");
        }
    }

    /**
     * 修改用户信息（用户名 / 邮箱 / 密码）
     */
    @PutMapping("/update-profile")
    public ResponseEntity<?> updateProfile(@RequestBody TouristUser user) {
        Optional<TouristUser> existingUser = userService.findByUsername(user.getUsername());
        if (existingUser.isPresent()) {
            TouristUser updatedUser = existingUser.get();
            if (user.getEmail() != null) updatedUser.setEmail(user.getEmail());
            if (user.getPassword() != null && !user.getPassword().isEmpty()) {
                updatedUser.setPassword(passwordEncoder.encode(user.getPassword())); // 重新加密密码
            }
            userService.saveUser(updatedUser);
            return ResponseEntity.ok("用户信息更新成功");
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body("用户不存在");
    }
}
