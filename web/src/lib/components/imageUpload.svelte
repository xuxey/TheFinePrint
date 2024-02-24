<script lang="ts">
	import Icon from '@iconify/svelte';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { API_URL } from '../constants';

	let files: FileList;

	const sendImageRequest = async () => {
		const response = await fetch(API_URL);
	};
</script>

<FileDropzone name="image-upload" bind:files accept="image/png, image/jpeg, image/jpg, image/tiff">
	<svelte:fragment slot="message">Upload an image</svelte:fragment>
	<svelte:fragment slot="meta">Choose from PNG, JPEG, JPG or Tiff</svelte:fragment>
</FileDropzone>
