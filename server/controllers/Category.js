const Category = require("../models/Category")

function getRandomInt(max) {
  return Math.floor(Math.random() * max)
}
exports.createCategory = async (req, res) => {
  try {
    const { name, description } = req.body
    if (!name) {
      return res
        .status(400)
        .json({ success: false, message: "All fields are required" })
    }
    const CategorysDetails = await Category.create({
      name: name,
      description: description,
    })
    console.log(CategorysDetails)
    return res.status(200).json({
      success: true,
      message: "Categorys Created Successfully",
    })
  } catch (error) {
    return res.status(500).json({
      success: true,
      message: error.message,
    })
  }
}

exports.showAllCategories = async (req, res) => {
  try {
    const allCategorys = await Category.find()
    res.status(200).json({
      success: true,
      data: allCategorys,
    })
  } catch (error) {
    return res.status(500).json({
      success: false,
      message: error.message,
    })
  }
}

exports.categoryPageDetails = async (req, res) => {
  try {
    const { categoryId } = req.body;

    // 1️⃣ Get selected category with published courses
    const selectedCategory = await Category.findById(categoryId)
      .populate({
        path: "courses",
        match: { status: "Published" },
        populate: "ratingAndReviews",
      })
      .exec();

    console.log("SELECTED COURSE", selectedCategory);

    if (!selectedCategory) {
      return res.status(404).json({
        success: false,
        message: "Category not found",
      });
    }

    // 2️⃣ If no courses in this category → return empty but DON'T crash
    if (!selectedCategory.courses || selectedCategory.courses.length === 0) {
      return res.status(200).json({
        success: true,
        data: {
          selectedCategory,
          differentCategory: null,
          mostSellingCourses: [],
        },
      });
    }

    // 3️⃣ Find OTHER categories (excluding selected)
    const categoriesExceptSelected = await Category.find({
      _id: { $ne: categoryId },
    });

    let differentCategory = null;

    // 👉 FIX: Only pick another category if it exists
    if (categoriesExceptSelected.length > 0) {
      const randomCategoryId =
        categoriesExceptSelected[getRandomInt(categoriesExceptSelected.length)]._id;

      differentCategory = await Category.findById(randomCategoryId)
        .populate({
          path: "courses",
          match: { status: "Published" },
        })
        .exec();
    }

    // 4️⃣ Get most selling courses safely
    const allCategories = await Category.find().populate({
      path: "courses",
      match: { status: "Published" },
    });

    const allCourses = allCategories.flatMap((cat) => cat.courses || []);

    const mostSellingCourses = allCourses
      .sort((a, b) => (b.sold || 0) - (a.sold || 0))
      .slice(0, 10);

    return res.status(200).json({
      success: true,
      data: {
        selectedCategory,
        differentCategory: differentCategory || { courses: [] }, // 🔥 IMPORTANT
        mostSellingCourses,
      },
    });
  } catch (error) {
    console.error("CATEGORY PAGE ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Internal server error",
      error: error.message,
    });
  }
};
