from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from chatbot import chat
from recommendations import get_recommendations
from task_manager import TaskManager

class ChatApp(App):
    def build(self):
        self.task_manager = TaskManager()
        self.layout = BoxLayout(orientation='vertical')
        
        self.mode = "chatbot"
        
        self.mode_label = Label(text="Mode: Chatbot")
        self.layout.add_widget(self.mode_label)

        self.chat_history = Label(size_hint_y=None, height=300, text_size=(400, None), valign='top')
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.layout.add_widget(self.chat_history)
        
        self.user_input = TextInput(size_hint_y=None, height=40)
        self.layout.add_widget(self.user_input)
        
        self.send_button = Button(text="Send", size_hint_y=None, height=40)
        self.send_button.bind(on_press=self.send_message)
        self.layout.add_widget(self.send_button)
        
        self.change_mode_button = Button(text="Change Mode", size_hint_y=None, height=40)
        self.change_mode_button.bind(on_press=self.change_mode)
        self.layout.add_widget(self.change_mode_button)
        
        return self.layout

    def send_message(self, instance):
        user_input = self.user_input.text
        self.update_chat_history(f"You: {user_input}")
        
        if self.mode == "chatbot":
            response = chat(user_input)
        elif self.mode == "recommendations":
            response = get_recommendations(user_input)
            #response = "\n".join(response)
        elif self.mode == "task_manager":
            if user_input.startswith("add task"):
                task = user_input[len("add task "):]
                response = self.task_manager.add_task(task)
            elif user_input.startswith("show tasks"):
                response = self.task_manager.show_tasks()
            elif user_input.startswith("remove task"):
                task = user_input[len("remove task "):]
                response = self.task_manager.remove_task(task)
            elif user_input.startswith("complete task"):
                task = user_input[len("complete task "):]
                response = self.task_manager.complete_task(task)
            else:
                response = "Task manager commands: add task, show tasks, remove task, complete task."
        else:
            response = "Invalid mode."
        
        self.update_chat_history(f"Bot: {response}")
        self.user_input.text = ""

    def update_chat_history(self, message):
        self.chat_history.text += f"\n{message}"
        self.chat_history.texture_update()
        self.chat_history.height = self.chat_history.texture_size[1]

    def change_mode(self, instance):
        if self.mode == "chatbot":
            self.mode = "recommendations"
        elif self.mode == "recommendations":
            self.mode = "task_manager"
        else:
            self.mode = "chatbot"
        self.mode_label.text = f"Mode: {self.mode.capitalize()}"

if __name__ == '__main__':
    ChatApp().run()

