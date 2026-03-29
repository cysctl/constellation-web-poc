<script lang="ts">
	import { wsStore } from '$lib/stores/websocket.svelte';

	let connStatus: 'connected' | 'disconnected' = $derived(
		wsStore.isConnected ? 'connected' : 'disconnected'
	);
</script>

<div class="inline-flex items-center gap-2">
	<div
		class="size-2 animate-pulse rounded-full {connStatus === 'connected'
			? 'bg-state-run'
			: 'bg-red-500'}"
	></div>

	<span class="hidden text-sm lg:block">
		{connStatus === 'connected' ? 'Connected' : 'Disconnected'}
	</span>
</div>
