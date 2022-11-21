import { ChatInputCommandInteraction } from 'discord.js';

export const beepHandler = async (
  interaction: ChatInputCommandInteraction,
): Promise<void> => {
  await interaction.reply({ content: 'boop!', ephemeral: true });
};
