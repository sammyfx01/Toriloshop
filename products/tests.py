from django.test import SimpleTestCase

from products.forms import CategoryForm, ProductForm


class FormTests(SimpleTestCase):
    def test_product_form_contains_expected_fields(self):
        form = ProductForm()
        self.assertIn("name", form.fields)
        self.assertIn("price", form.fields)
        self.assertIn("stock", form.fields)
        self.assertIn("is_available", form.fields)
        self.assertIn("Category", form.fields)

    def test_category_form_contains_expected_fields(self):
        form = CategoryForm()
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
