from django.db import models

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()        # ID of the product being reviewed
    user_id = models.IntegerField()           # ID of the user who posted the review
    rating = models.IntegerField()            # Rating given by the user (1-5 stars, for example)
    comment = models.TextField(blank=True)    # Optional textual comment provided by the user
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was posted

    # Additional attributes
    helpful_count = models.IntegerField(default=0)   # Number of users who found the review helpful
    is_verified = models.BooleanField(default=False) # Whether the review is verified (e.g., by admin)

    def __str__(self):
        return f"Review {self.review_id} for Product {self.product_id} by User {self.user_id}"

    def add_review(self, product_id, user_id, rating, comment=None):
        # Method to add a new review
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        if comment:
            self.comment = comment
        self.save()

    @classmethod
    def get_reviews_for_product(cls, product_id):
        # Method to retrieve all reviews for a specific product
        return cls.objects.filter(product_id=product_id).order_by('-timestamp')

    def delete_review(self):
        # Method to delete the review
        self.delete()

    def mark_as_helpful(self):
        # Method to mark the review as helpful (increment helpful_count)
        self.helpful_count += 1
        self.save()

    def mark_as_verified(self):
        # Method to mark the review as verified
        self.is_verified = True
        self.save()
