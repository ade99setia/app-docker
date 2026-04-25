from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps


MAX_FILE_SIZE_BYTES = 500 * 1024
INPUT_FOLDER = Path(__file__).resolve().parent / "teacher_photos"
OUTPUT_FOLDER = INPUT_FOLDER
SUPPORTED_IMAGE_EXTENSIONS = {
	".png",
	".bmp",
	".webp",
	".tif",
	".tiff",
	".gif",
	".jfif",
	".jpeg",
	".jpg",
}
JPEG_EXTENSIONS = {".jpg", ".jpeg", ".jfif"}
MAX_DIMENSION = 1600
MIN_QUALITY = 55
INITIAL_QUALITY = 92
QUALITY_STEP = 5
RESIZE_STEP = 0.9


@dataclass
class ProcessResult:
	source: Path
	output: Path
	size_bytes: int
	face_found: bool


def load_image(image_path: Path) -> Image.Image:
	image = Image.open(image_path)
	image = ImageOps.exif_transpose(image)

	if image.mode in {"RGBA", "LA"}:
		background = Image.new("RGB", image.size, (255, 255, 255))
		background.paste(image, mask=image.getchannel("A"))
		return background

	if image.mode != "RGB":
		return image.convert("RGB")

	return image


def detect_face_box(image: Image.Image) -> tuple[int, int, int, int] | None:
	rgb_array = np.array(image)
	bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
	gray = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2GRAY)

	cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
	face_cascade = cv2.CascadeClassifier(str(cascade_path))

	faces = face_cascade.detectMultiScale(
		gray,
		scaleFactor=1.08,
		minNeighbors=6,
		minSize=(90, 90),
	)

	if len(faces) == 0:
		return None

	largest_face = max(faces, key=lambda face: face[2] * face[3])
	return tuple(int(value) for value in largest_face)


def clamp_crop_box(
	left: float,
	top: float,
	crop_width: float,
	crop_height: float,
	image_width: int,
	image_height: int,
) -> tuple[int, int, int, int]:
	left = max(0.0, min(left, image_width - crop_width))
	top = max(0.0, min(top, image_height - crop_height))
	right = min(image_width, left + crop_width)
	bottom = min(image_height, top + crop_height)
	return int(round(left)), int(round(top)), int(round(right)), int(round(bottom))


def crop_toward_face(image: Image.Image) -> tuple[Image.Image, bool]:
	face_box = detect_face_box(image)
	if face_box is None:
		return image, False

	image_width, image_height = image.size
	aspect_ratio = image_width / image_height
	x, y, width, height = face_box

	target_crop_width = width / 0.38
	target_crop_height = height / 0.45

	if target_crop_width / target_crop_height > aspect_ratio:
		target_crop_height = target_crop_width / aspect_ratio
	else:
		target_crop_width = target_crop_height * aspect_ratio

	target_crop_width = min(float(image_width), target_crop_width)
	target_crop_height = min(float(image_height), target_crop_height)

	face_center_x = x + (width / 2)
	face_center_y = y + (height * 0.46)

	left = face_center_x - (target_crop_width / 2)
	top = face_center_y - (target_crop_height * 0.42)

	crop_box = clamp_crop_box(
		left,
		top,
		target_crop_width,
		target_crop_height,
		image_width,
		image_height,
	)

	return image.crop(crop_box), True


def limit_dimensions(image: Image.Image) -> Image.Image:
	width, height = image.size
	largest_side = max(width, height)
	if largest_side <= MAX_DIMENSION:
		return image

	scale = MAX_DIMENSION / largest_side
	new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
	return image.resize(new_size, Image.Resampling.LANCZOS)


def compress_to_target(image: Image.Image) -> tuple[bytes, int]:
	working_image = image

	while True:
		for quality in range(INITIAL_QUALITY, MIN_QUALITY - 1, -QUALITY_STEP):
			buffer = io.BytesIO()
			working_image.save(
				buffer,
				format="JPEG",
				quality=quality,
				optimize=True,
				progressive=True,
				subsampling="4:2:0",
			)
			data = buffer.getvalue()
			if len(data) <= MAX_FILE_SIZE_BYTES:
				return data, quality

		resized_width = max(1, int(working_image.width * RESIZE_STEP))
		resized_height = max(1, int(working_image.height * RESIZE_STEP))

		if resized_width == working_image.width and resized_height == working_image.height:
			buffer = io.BytesIO()
			working_image.save(buffer, format="JPEG", quality=MIN_QUALITY, optimize=True)
			return buffer.getvalue(), MIN_QUALITY

		working_image = working_image.resize(
			(resized_width, resized_height),
			Image.Resampling.LANCZOS,
		)


def process_image(image_path: Path) -> ProcessResult:
	image = load_image(image_path)
	image, face_found = crop_toward_face(image)
	image = limit_dimensions(image)

	jpg_data, _quality = compress_to_target(image)
	output_path = OUTPUT_FOLDER / f"{image_path.stem}.jpg"
	output_path.write_bytes(jpg_data)

	return ProcessResult(
		source=image_path,
		output=output_path,
		size_bytes=len(jpg_data),
		face_found=face_found,
	)


def should_process_file(image_path: Path) -> bool:
	if image_path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
		return False

	if image_path.suffix.lower() not in JPEG_EXTENSIONS:
		return True

	return image_path.stat().st_size > MAX_FILE_SIZE_BYTES


def main() -> None:
	if not INPUT_FOLDER.exists():
		raise FileNotFoundError(f"Folder foto tidak ditemukan: {INPUT_FOLDER}")

	source_files = sorted(
		path
		for path in INPUT_FOLDER.iterdir()
		if path.is_file() and should_process_file(path)
	)

	if not source_files:
		print(f"Tidak ada file yang perlu dikonversi di folder: {INPUT_FOLDER}")
		return

	success_count = 0
	fallback_count = 0

	for image_path in source_files:
		try:
			result = process_image(image_path)
			success_count += 1
			if not result.face_found:
				fallback_count += 1

			print(
				f"[OK] {result.source.name} -> {result.output.name} | "
				f"{result.size_bytes / 1024:.1f} KB | "
				f"face_detected={'yes' if result.face_found else 'no'}"
			)
		except Exception as error:
			print(f"[ERROR] {image_path.name}: {error}")

	print("\nSelesai memproses foto.")
	print(f"Total sukses : {success_count}")
	print(f"Tanpa wajah  : {fallback_count}")
	print(f"Output JPG   : {OUTPUT_FOLDER}")


if __name__ == "__main__":
	main()
