def edit_style_by_niche(niche: str, video_path: str) -> str:
    if niche == "carros":
        edited_video = f"edited_{video_path}_carros.mp4"
    elif niche == "nutricao":
        edited_video = f"edited_{video_path}_nutricao.mp4"
    else:
        edited_video = f"edited_{video_path}_default.mp4"
    return edited_video
