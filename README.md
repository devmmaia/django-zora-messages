# django_zora_messages

### A simple Django app to manage the messages displayed in your website via database.

Everytime you load a new key message in your django application, the register will be created in a database table, where you can translate it and write instructions to help your helpdesk and developers teams. These changes can be made via Django admin.

Detailed documentation is in the "docs" directory.

### Quick start

1. Add "django_zora_messages" to your INSTALLED_APPS setting like this:
```python
		INSTALLED_APPS = [

		'...',

		'django_zora_messages',

		]
```
  
  
  

2. Run    **`python manage.py migrate`** to create the models.

3. Import and use the load method:  
    ```python
    from django_zora_messages.utils import get_message as msg
    print (msg("key.not.found.error").value)
    ```

4. Test your view. You should see the key used in your website.

  

5. Start the development server and visit http://127.0.0.1:8000/admin/ 
6. Change the message to whatever You want. Remember to supply the detailed message and instructions for your team. (you'll need the Admin app enabled).