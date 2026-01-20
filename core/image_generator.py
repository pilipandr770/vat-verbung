#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image Generator
Generates B2B marketing images using DALL-E-3 with professional prompts
"""

import os
import logging
import requests
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)
load_dotenv()

class ImageGenerator:
    """DALL-E-3 image generator for B2B marketing content with professional prompts"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.image_model = os.getenv('IMAGE_MODEL', 'dall-e-3')
        self.image_size = "1024x1024"
        
        self.images_dir = Path("data/generated_images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            logger.warning("⚠️  OPENAI_API_KEY not configured - using placeholder images")
            self.enabled = False
        else:
            self.enabled = True
            logger.info("✅ Image generator initialized with DALL-E-3 and professional prompts")
    
    def generate_image(self, topic: str, content_type: str, description: Optional[str] = None) -> Optional[str]:
        """Generate image using DALL-E-3 or fallback to placeholder"""
        
        if not self.enabled:
            placeholder_gen = PlaceholderImageGenerator()
            return placeholder_gen.generate_placeholder(topic, content_type)
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = self._create_image_prompt(topic, content_type, description)
            logger.info(f"📸 Generating professional image for {topic}/{content_type}...")
            
            response = client.images.generate(
                model=self.image_model,
                prompt=prompt,
                n=1,
                size=self.image_size,
                quality="standard"
            )
            
            image_url = response.data[0].url
            image_path = self._download_and_save_image(image_url, topic, content_type)
            logger.info(f"✅ Professional image generated: {image_path}")
            
            return str(image_path)
            
        except ImportError:
            logger.error("❌ openai library not installed - using placeholder")
            placeholder_gen = PlaceholderImageGenerator()
            return placeholder_gen.generate_placeholder(topic, content_type)
        except Exception as e:
            logger.error(f"❌ Error generating DALL-E image: {str(e)} - using placeholder")
            placeholder_gen = PlaceholderImageGenerator()
            return placeholder_gen.generate_placeholder(topic, content_type)
    
    def _create_image_prompt(self, topic: str, content_type: str, description: Optional[str] = None) -> str:
        """Create professional DALL-E-3 prompts optimized for B2B German market"""
        
        prompts = {
            # AUTOMATION - Process Efficiency & Cost Reduction
            ("automation", "pain"): 
                "Professional B2B infographic showing business process transformation. "
                "Left side: chaotic manual office work with tangled process flows, stressed employees, scattered papers, time-waste symbols. "
                "Right side: streamlined automated processes with clean data flows, efficient team, success checkmarks. "
                "Modern flat design, professional blue-green color scheme, German corporate aesthetic, "
                "suitable for LinkedIn B2B marketing. Clean background, high quality 1024x1024.",
            
            ("automation", "warning"):
                "Professional business warning illustration about automation necessity. "
                "Show businessman at crossroads: left path shows company stagnation with competitors racing ahead (blurred motion), "
                "right path shows efficiency through automation with clear upward trend. "
                "Modern corporate design with urgency elements, digital transformation theme. "
                "Professional red-orange accent colors, clean lines. LinkedIn B2B suitable.",
            
            ("automation", "use_case"):
                "Professional case study visualization of manufacturing company's digital transformation. "
                "Before (left): cluttered warehouse with manual processes, red error symbols, inefficiency indicators. "
                "After (right): organized automated system with robots, digital controls, green success indicators, metrics improvement. "
                "Professional 3D-style illustration, German B2B corporate design, suitable for case study presentations.",
            
            ("automation", "explanation"):
                "Professional educational infographic explaining RPA and process automation. "
                "Show layered architecture: data input → automation engine (with gears/circuits metaphor) → output results. "
                "Include clean icons for automation technologies (AI, ML, workflow engines). "
                "Modern flat design with clear visual hierarchy, professional German corporate colors (blue/white/grey). "
                "Suitable for LinkedIn educational content and technical audiences.",
            
            # COMPLIANCE - Regulatory & Legal Risk Management
            ("compliance", "pain"):
                "Professional illustration showing regulatory compliance burden. "
                "Manager surrounded by thick stacks of legal documents, regulations, warning labels, complex process flows. "
                "Visual elements conveying confusion, complexity, and risk. Modern corporate design with muted, serious colors. "
                "German B2B aesthetic. Professional tone suitable for financial/legal industry LinkedIn posts.",
            
            ("compliance", "warning"):
                "Professional regulatory risk visualization. "
                "Show corporate building with structural issues: cracks appearing in foundation, regulatory red flags hovering above, "
                "warning symbols. Show consequences of non-compliance. Professional illustration in corporate style with "
                "red-orange warning accents. German B2B market design, serious professional tone.",
            
            ("compliance", "use_case"):
                "Professional success story: company achieving systematic compliance. "
                "Before: scattered, unorganized compliance attempts with documents scattered. "
                "After: organized certified system with checkmarks, compliance badges, certified seals. "
                "Professional, reassuring design. Clean modern flat style suitable for B2B LinkedIn. Show improvement metrics.",
            
            ("compliance", "explanation"):
                "Professional infographic showing compliance framework as process flow. "
                "Show: Regulatory requirements → Policies → Implementation → Audit → Certification. "
                "Each layer clearly illustrated with relevant icons and connecting arrows. "
                "Professional educational style with German corporate colors (blue/grey). "
                "Suitable for institutional and regulatory-focused LinkedIn content.",
            
            # DIGITAL TRANSFORMATION - Technology & Innovation
            ("digitalization", "pain"):
                "Professional illustration of outdated business operations. "
                "Show old-style office: paper files, fax machines, spreadsheets, manual data entry, disconnected systems. "
                "Visual chaos with arrows pointing in wrong directions, showing inefficiency and lost opportunities. "
                "Modern flat design with muted colors, professional German B2B aesthetic.",
            
            ("digitalization", "warning"):
                "Professional digital transformation urgency visualization. "
                "Show competitor with digital advantage racing ahead (motion blur) while traditional company falls behind. "
                "Illustrate market disruption theme with forward momentum visual elements. "
                "Professional B2B design suitable for urgency messaging and digital transformation initiatives.",
            
            ("digitalization", "use_case"):
                "Professional digital transformation journey visualization. "
                "Show company evolution: paper-based office → hybrid systems → cloud-native system (multi-stage flow). "
                "Include process flow, employee adaptation, modern technology stack. "
                "Professional and modern design, German corporate aesthetic suitable for case studies.",
            
            ("digitalization", "explanation"):
                "Professional digital ecosystem infographic. "
                "Show central business connected to: cloud services, data analytics, automation platform, mobile solutions. "
                "Each component with clear icons and labels. Modern flat design with professional corporate colors. "
                "Suitable for technical B2B audience on LinkedIn.",
            
            # COST OPTIMIZATION - Financial Efficiency
            ("costs", "pain"):
                "Professional financial visualization showing cost structure. "
                "Show pie charts with cost breakdown, highlight unnecessary expenses in red, add waste symbols, "
                "show inefficient resource allocation. Include trend chart showing budget overruns. "
                "Professional financial infographic style suitable for CFO and finance team audience. "
                "German B2B corporate design.",
            
            ("costs", "warning"):
                "Professional cost risk visualization. "
                "Show rising cost trend line with exponential growth if action not taken, include warning indicators, "
                "show profit margin being squeezed. Illustrate financial consequences visually. "
                "Professional serious design with red warning elements and metric visualization.",
            
            ("costs", "use_case"):
                "Professional ROI success story visualization. "
                "Show company cost reduction through optimization: before/after budget comparison, "
                "highlight savings (green), show reinvestment opportunities. "
                "Professional financial design with positive visual tone. Suitable for finance teams on LinkedIn.",
            
            ("costs", "explanation"):
                "Professional cost structure breakdown and optimization framework. "
                "Show pie chart with cost categories and optimization levers, list cost reduction techniques with percentages, "
                "highlight quick wins. Educational financial infographic with professional German corporate design.",
            
            # WORKFLOWS - Process Improvement
            ("workflows", "pain"):
                "Professional chaotic workflow visualization. "
                "Show tangled process flows, bottleneck points, duplicate work, manual handoffs between teams, "
                "waiting symbols (hourglasses). Visual representation of process inefficiency and complexity. "
                "Modern illustration style, professional B2B design.",
            
            ("workflows", "warning"):
                "Professional process bottleneck impact visualization. "
                "Show pipeline with blockage points, team members waiting, delayed projects, cascade failure effects. "
                "Warning visualization showing consequences of poor workflow design. Professional serious design style.",
            
            ("workflows", "use_case"):
                "Professional workflow optimization success story. "
                "Before: complex tangled process flows. After: clean streamlined workflow with clear stages, "
                "show improvement indicators (cycle time reduced %, error reduction, collaboration improved). "
                "Professional before/after comparison design.",
            
            ("workflows", "explanation"):
                "Professional workflow optimization framework infographic. "
                "Show process mapping: current state → ideal state → optimization opportunities. "
                "Clean visual representation with icons for each process step and connecting flows. "
                "Educational infographic style, professional German B2B design.",
            
            # OPERATIONS - Operational Excellence
            ("operations", "pain"):
                "Professional operational chaos illustration. "
                "Show scattered resources, poor coordination, quality issues (red X marks), delivery delays (red clock symbols), "
                "customer dissatisfaction indicators. Illustrate operational pain points clearly. Professional serious design.",
            
            ("operations", "warning"):
                "Professional operational risk visualization. "
                "Show operations failing under load, quality deterioration visible, customer churn indicators, "
                "competitive disadvantage growing. Warning illustration of poor operations consequences.",
            
            ("operations", "use_case"):
                "Professional operational excellence success story. "
                "Show company transformation from chaotic to organized operations with improved metrics: "
                "on-time delivery %, quality scores improvement, customer satisfaction increase. "
                "Before/after visualization with professional inspiring design.",
            
            ("operations", "explanation"):
                "Professional operational excellence framework infographic. "
                "Show: Key Performance Indicators (KPIs) → Process Optimization → Quality Management → "
                "Continuous Improvement Cycle. Include icons and best practices. "
                "Educational design, professional German corporate aesthetic.",
            
            # DATA - Data-Driven Decision Making
            ("data", "pain"):
                "Professional data chaos illustration. "
                "Show multiple disconnected data sources, incomplete information, manual analysis bottlenecks, "
                "decision makers without clear insights. Illustrate information silos and poor data governance. "
                "Professional corporate design showing organizational challenge.",
            
            ("data", "warning"):
                "Professional data-driven competitor advantage visualization. "
                "Show business making decisions without data analytics falling behind, competitor with data intelligence "
                "moving ahead. Show market disadvantage from poor data decisions.",
            
            ("data", "use_case"):
                "Professional data-driven transformation story. "
                "Show company using analytics: discover insights → optimize decisions → improve business outcomes. "
                "Include dashboard/analytics visualization, improved metrics display, successful decision outcomes. "
                "Professional modern design.",
            
            ("data", "explanation"):
                "Professional data analytics ecosystem infographic. "
                "Show complete value chain: Data sources → Collection → Processing → Analytics Engine → Insights → "
                "Strategic Decisions. Include visualization, reporting, and BI tools. Educational design style.",
        }
        
        topic_clean = topic.lower().replace('contentopic.', '')
        content_type_clean = content_type.lower().replace('contenttype.', '')
        prompt_key = (topic_clean, content_type_clean)
        
        base_prompt = prompts.get(prompt_key)
        
        if not base_prompt:
            base_prompt = (
                f"Professional B2B business illustration about {topic} and {content_type}. "
                f"Modern corporate design with professional colors. Clean, modern aesthetic suitable for "
                f"LinkedIn B2B marketing. German business aesthetic."
            )
        
        quality_directives = (
            " || QUALITY: High resolution 1024x1024, photo-realistic or modern flat design, "
            "no watermarks, clean white/light grey background, LinkedIn-professional, corporate-appropriate. "
            "German business aesthetic. Suitable for global B2B marketing."
        )
        
        return base_prompt + quality_directives
    
    def _download_and_save_image(self, image_url: str, topic: str, content_type: str) -> Path:
        """Download image from URL and save locally"""
        
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{topic}_{content_type}_{timestamp}.png"
            filepath = self.images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"✅ Image downloaded and saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Error downloading image: {str(e)}")
            return None
    
    def is_enabled(self) -> bool:
        """Check if DALL-E image generation is enabled"""
        return self.enabled

class PlaceholderImageGenerator:
    """Fallback: Generate placeholder images using PIL when DALL-E is unavailable"""
    
    def __init__(self):
        self.images_dir = Path("data/generated_images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        logger.info("✅ Placeholder image generator initialized")
    
    def generate_placeholder(self, topic: str, content_type: str) -> Optional[str]:
        """Generate a simple placeholder image"""
        
        try:
            from PIL import Image, ImageDraw
            
            img = Image.new('RGB', (1024, 1024), color=(240, 240, 245))
            draw = ImageDraw.Draw(img)
            
            colors = {
                'automation': [(100, 150, 50), (70, 120, 30)],
                'compliance': [(50, 100, 200), (30, 70, 170)],
                'digitalization': [(150, 100, 50), (120, 75, 30)],
                'costs': [(200, 50, 50), (150, 30, 30)],
                'workflows': [(100, 100, 150), (70, 70, 120)],
                'operations': [(150, 100, 50), (120, 75, 30)],
                'data': [(100, 150, 150), (70, 120, 120)],
            }
            
            topic_lower = topic.lower()
            color_pair = colors.get(topic_lower, [(100, 100, 100), (70, 70, 70)])
            
            # Draw gradient
            for i in range(256):
                ratio = i / 256
                r = int(color_pair[0][0] * (1 - ratio) + color_pair[1][0] * ratio)
                g = int(color_pair[0][1] * (1 - ratio) + color_pair[1][1] * ratio)
                b = int(color_pair[0][2] * (1 - ratio) + color_pair[1][2] * ratio)
                draw.rectangle([(0, i*4), (1024, (i+1)*4)], fill=(r, g, b))
            
            text = f"{topic.upper()}\n{content_type.upper()}"
            draw.text((512, 512), text, fill=(255, 255, 255), anchor="mm")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{topic}_{content_type}_{timestamp}_placeholder.png"
            filepath = self.images_dir / filename
            
            img.save(filepath)
            logger.info(f"✅ Placeholder image created: {filepath}")
            
            return str(filepath)
            
        except ImportError:
            logger.error("❌ PIL (Pillow) not installed")
            return None
        except Exception as e:
            logger.error(f"❌ Error creating placeholder: {str(e)}")
            return None
