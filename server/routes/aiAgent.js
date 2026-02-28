// Importing necessary modules and packages
const express = require("express");
const router = express.Router();

// Import controllers
const {
  getUserContext,
  saveRecommendation,
  getRecommendations,
  updateProgress
} = require("../controllers/aiAgent");

// Import middleware
const { auth } = require("../middleware/auth");

// ********************************************************************************************************
//                                      AI Agent Routes
// ********************************************************************************************************

/**
 * @route   GET /api/v1/aiagent/user-context/:userId
 * @desc    Get user context including profile and enrolled courses
 * @access  Public (can be protected with auth middleware if needed)
 */
router.get("/user-context/:userId", getUserContext);

/**
 * @route   POST /api/v1/aiagent/save-recommendation
 * @desc    Save assessment recommendation for user
 * @access  Protected
 */
router.post("/save-recommendation", auth, saveRecommendation);

/**
 * @route   GET /api/v1/aiagent/recommendations/:userId
 * @desc    Get saved recommendations for user
 * @access  Protected
 */
router.get("/recommendations/:userId", auth, getRecommendations);

/**
 * @route   POST /api/v1/aiagent/update-progress
 * @desc    Update user's assessment progress
 * @access  Protected
 */
router.post("/update-progress", auth, updateProgress);

module.exports = router;
