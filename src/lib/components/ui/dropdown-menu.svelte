<script lang="ts">
	interface DropdownMenuProps {
		deviceType: string;
		deviceName: string;
		items: string[];
		onSelect?: (item: string) => void;
	}

	let { deviceType, deviceName, items, onSelect }: DropdownMenuProps = $props();

	let isOpen = $state(false);
	let x = $state(0);
	let y = $state(0);

	export function open(e: MouseEvent) {
		e.preventDefault();
		x = e.clientX;
		y = e.clientY;
		isOpen = true;
	}

	export function close() {
		isOpen = false;
	}
</script>

<svelte:window onclick={() => isOpen && close()} onkeydown={(e) => e.key === 'Escape' && close()} />

{#if isOpen}
	<ul
		class="fixed z-50 min-w-40 overflow-hidden rounded-xl border border-border bg-card shadow-lg"
		style="left: {x}px; top: {y}px;"
		role="menu"
	>
		{#if deviceType && deviceName}
			<li class="border-b border-border px-4 py-2 select-none [&>span]:text-muted-foreground">
				<span class="font-medium">{deviceName}</span>
				<span>({deviceType})</span>
			</li>
		{/if}

		{#each items as item}
			{#if item === '-'}
				<li class="border-t border-border"></li>
			{:else}
				<li>
					<button
						class="w-full cursor-pointer px-4 py-2 text-left text-sm text-card-foreground transition-colors hover:bg-border"
						role="menuitem"
						onclick={(e) => {
							e.stopPropagation();
							onSelect?.(item);
							close();
						}}
					>
						{item}
					</button>
				</li>
			{/if}
		{/each}
	</ul>
{/if}
