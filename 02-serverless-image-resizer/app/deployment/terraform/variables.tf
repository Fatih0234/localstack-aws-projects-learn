variable "gemini_api_key" {
  description = "API key for Google Gemini image generation API"
  type        = string
  sensitive   = true
  default     = ""
}
