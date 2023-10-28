import discord
from discord.ext import commands


class file_input(commands.Cog):
    def __init__(self, bot):
        self.bot = bot









    #yes no menu which returns true or false value. Add to any message

    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=5)
            self.value = None

        async def on_timeout(self):
            self.stop()

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            for i in self.children:
                i.disabled = True
            self.value = True
            await interaction.response.edit_message(view=self)
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            for i in self.children:
                i.disabled = True
            self.value = False
            await interaction.response.edit_message(view=self)
            self.stop()












    #discord listener which looks for any attachments in messages

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments == None:
            return
        favourable_files = [i for i in message.attachments if i.filename.split(".")[1] in ["gif", "png", "jpeg", "jpg", "mp3", "mp4"]]
        if len(favourable_files) == 0:
            return

        view = self.Confirm()




        #asking if the user actually wants to mint a NFT

        msg = await message.channel.send('Do you want to mint NFT?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value == True:
            pass
        elif view.value == False:
            await msg.edit(content="Ok I won't mint a NFT", view=None)
            return
        else:
            await msg.edit(content="I guess you didn't want to mint a NFT", view=None)
            return






        #choose which file to mint

        #store the file to mint in a variable
        file_to_mint = None

        #if only one favorable file, choose it
        if len(favourable_files) == 1:
            file_to_mint = favourable_files[0]


        #give user a list of favorable files and then ask them to choose one.
        else:
            #adding embeds with a display of the image
            embeds = []
            for i in range(len(message.attachments)):
                embed = None
                if message.attachments[i].filename.split('.')[1] in ["png", "jpg", "jpeg"]:
                    embed = discord.Embed(title=str(i+1)+'.')
                    embed.set_thumbnail(url =message.attachments[i])
                else:
                    embed = discord.Embed(title=str(i+1)+". "+message.attachments[i].filename)
                embeds.append(embed)

            class take_NFT_details(discord.ui.Modal):
                def __init__(self):
                    super().__init__(title= "Give details for your NFT!!!")
                    self.name = discord.ui.TextInput(
                        label="Enter a name for the NFT",
                        min_length=3,
                        max_length=60,
                    )
                    self.add_item(self.name)

                    self.description = discord.ui.TextInput(
                        label="Enter a description for the NFT",
                        min_length=5,
                        max_length=60,
                    )
                    self.add_item(self.description)

                async def on_submit(self, interaction):
                    print(interaction.content)

            #adding a view with buttons for each file
            #class to define a view with a value parameter as well which will store which button was chosen by mapping the unique id
            class choose_buttons(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=5)
                    self.value = None
                    self.button_ids = []

                async def callback_choose_button(self, interaction):
                    modal = take_NFT_details()
                    await interaction.response.send_modal(modal)
                    self.stop()
                    self.value = self.button_ids.index(interaction.data['custom_id'])


            view = choose_buttons()



            #we'll store the custom ids of all buttons and when callback function is invoked, we'll map the custom id with the position in the list to check which file was chosen
            for i in range(len(favourable_files)):
                x = discord.ui.Button(label=str(i+1), style=discord.ButtonStyle.blurple)
                x.callback = view.callback_choose_button
                view.button_ids.append(x.custom_id)
                view.add_item(x)

            await msg.edit(embeds= embeds, view=view)
            await view.wait()
            if view.value != None:
                file_to_mint = favourable_files[view.value]

            if file_to_mint == None:
                await msg.edit(view=None, content="Looks like you didn't respond in time. Try again if you want to mint the NFT.", embeds=[])
                return




        await msg.edit(content=file_to_mint.url, view=view, embeds=[])


