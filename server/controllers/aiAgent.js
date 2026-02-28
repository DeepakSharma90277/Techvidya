/**
 * AI Agent Controller
 * Handles AI agent related operations including user context and recommendations
 */

const User = require("../models/User");
const Course = require("../models/Course");
const CourseProgress = require("../models/CourseProgress");

/**
 * Get user context including profile and enrolled courses
 * 
 * @route   GET /api/v1/aiagent/user-context/:userId
 * @access  Public
 */
exports.getUserContext = async (req, res) => {
  try {
    const { userId } = req.params;

    // Validate user ID
    if (!userId) {
      return res.status(400).json({
        success: false,
        message: "User ID is required"
      });
    }

    // Find user and populate necessary fields
    const user = await User.findById(userId)
      .populate({
        path: "courses",
        populate: {
          path: "instructor",
          select: "firstName lastName"
        }
      })
      .populate("additionalDetails")
      .exec();

    if (!user) {
      return res.status(404).json({
        success: false,
        message: "User not found"
      });
    }

    // Get course progress for enrolled courses
    const courseProgress = await CourseProgress.find({
      userId: userId
    });

    // Build progress map
    const progressMap = {};
    courseProgress.forEach(cp => {
      progressMap[cp.courseID] = cp.completedVideos ? cp.completedVideos.length : 0;
    });

    // Format user data
    const userData = {
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.email,
      accountType: user.accountType,
      courses: user.courses.map(course => ({
        _id: course._id,
        courseName: course.courseName,
        courseDescription: course.courseDescription,
        instructor: course.instructor ? 
          `${course.instructor.firstName} ${course.instructor.lastName}` : 
          "Unknown",
        thumbnail: course.thumbnail,
        price: course.price,
        progress: progressMap[course._id] || 0,
        totalVideos: course.courseContent ? course.courseContent.length : 0
      })),
      profileData: user.additionalDetails,
      completed_assessments: 0, // TODO: Implement assessment tracking
      avg_score: 0, // TODO: Implement score tracking
      streak: 0 // TODO: Implement streak tracking
    };

    return res.status(200).json({
      success: true,
      message: "User context retrieved successfully",
      data: userData
    });

  } catch (error) {
    console.error("Error getting user context:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to get user context",
      error: error.message
    });
  }
};

/**
 * Save assessment recommendation for user
 * 
 * @route   POST /api/v1/aiagent/save-recommendation
 * @access  Protected
 */
exports.saveRecommendation = async (req, res) => {
  try {
    const { userId, assessment } = req.body;

    // Validate input
    if (!userId || !assessment) {
      return res.status(400).json({
        success: false,
        message: "User ID and assessment data are required"
      });
    }

    // Find user
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: "User not found"
      });
    }

    // TODO: Create a new model for storing recommendations
    // For now, we can store in user's additionalDetails or create a new collection
    
    // This is a placeholder response
    return res.status(200).json({
      success: true,
      message: "Recommendation saved successfully",
      data: {
        userId,
        assessment,
        savedAt: new Date()
      }
    });

  } catch (error) {
    console.error("Error saving recommendation:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to save recommendation",
      error: error.message
    });
  }
};

/**
 * Get saved recommendations for user
 * 
 * @route   GET /api/v1/aiagent/recommendations/:userId
 * @access  Protected
 */
exports.getRecommendations = async (req, res) => {
  try {
    const { userId } = req.params;

    // Validate user ID
    if (!userId) {
      return res.status(400).json({
        success: false,
        message: "User ID is required"
      });
    }

    // TODO: Fetch recommendations from database
    // For now, return empty array
    
    return res.status(200).json({
      success: true,
      message: "Recommendations retrieved successfully",
      data: []
    });

  } catch (error) {
    console.error("Error getting recommendations:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to get recommendations",
      error: error.message
    });
  }
};

/**
 * Update user's assessment progress
 * 
 * @route   POST /api/v1/aiagent/update-progress
 * @access  Protected
 */
exports.updateProgress = async (req, res) => {
  try {
    const { userId, assessmentId, score, completed } = req.body;

    // Validate input
    if (!userId || !assessmentId) {
      return res.status(400).json({
        success: false,
        message: "User ID and assessment ID are required"
      });
    }

    // Find user
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: "User not found"
      });
    }

    // TODO: Update assessment progress in database
    
    return res.status(200).json({
      success: true,
      message: "Progress updated successfully",
      data: {
        userId,
        assessmentId,
        score,
        completed,
        updatedAt: new Date()
      }
    });

  } catch (error) {
    console.error("Error updating progress:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to update progress",
      error: error.message
    });
  }
};
