<script lang="ts">
	import { Sun, Moon } from '@lucide/svelte';

	let theme: 'light' | 'dark' = $state('dark');

	$effect(() => {
		if (theme == 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	});
</script>

<button
	class="h-fit cursor-pointer rounded-lg p-1 text-muted-foreground transition-colors hover:bg-border active:scale-95"
	onclick={() => (theme = theme == 'light' ? 'dark' : 'light')}
>
	{#if theme == 'dark'}
		<Moon size={17} />
	{:else}
		<Sun size={17} />
	{/if}
</button>
