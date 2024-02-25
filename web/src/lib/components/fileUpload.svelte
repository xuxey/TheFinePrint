<script lang="ts">
	import Icon from '@iconify/svelte';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { API_URL } from '$lib/constants';

	let files: FileList;

	const sendImageRequest = async () => {
		const response = await fetch(API_URL);
	};
</script>

<FileDropzone name="file-upload" bind:files accept="application/pdf">
	<svelte:fragment slot="message">Upload a Document</svelte:fragment>
	<svelte:fragment slot="meta">We currently support PDFs</svelte:fragment>
</FileDropzone>
